import httpx
import asyncio
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LinkResult:
    url: str
    status_code: int | None = None
    final_url: str | None = None
    redirects: int | None = None
    error: str | None = None
    func_time: float | None = None
    AsyncClient_time: float | None = None

W_URL = 30
W_STATUS = 10
W_FINAL_URL = 30
W_REDIRECTS = 10
W_ERROR = 40
W_FUNC_TIME = 10
W_ASYNCCLIENT_TIME = 10

timeout_func = 10
timeout_response = 5

URL = "URLS.txt"


def get_urls_from_file(path: str):
    p = Path(path)
    try:

        with p.open() as f:
            lines = f.readlines()
        clean_lines = [line.strip(', \n"') for line in lines if line.strip(', \n"') and not line.strip().startswith("#")]
        return clean_lines
    except Exception as e:
        print(f"File {path} not found")
        raise str(e).strip()


ROW_TEMPLATE = (
    f"{{url:<{W_URL}}} | "
    f"{{status:<{W_STATUS}}} | "
    f"{{final_url:<{W_FINAL_URL}}} | "
    f"{{redirects:<{W_REDIRECTS}}} | "
    f"{{error:<{W_ERROR}}} | "
    f"{{func_time:<{W_FUNC_TIME}}} | "
    f"{{async_time:<{W_ASYNCCLIENT_TIME}}}"
)


def format_cell(value, width, is_error=False):
    if value is None:
        return "ОК" if is_error else "-"
    
    # Для времени добавляем суффикс "s"
    if isinstance(value, float):
        string_value = f"{value}s"
    else:
        string_value = str(value)
        
    # Если строка длиннее колонки — аккуратно обрезаем её
    if len(string_value) > width:
        return string_value[:width - 3] + "..."
    return string_value


async def check_link(url: str, client):
    result = LinkResult(url=url)
    if not url or not url.strip():
        result.error = "Link not provided"
        return result
    try:
        async with asyncio.timeout(timeout_func):
            start_1 = time.perf_counter()
            start_2 = time.perf_counter()
            try:
                r = await client.get(url, follow_redirects=True, timeout=timeout_response)
                result.status_code = r.status_code
                result.final_url = str(r.url)
                result.redirects = len(r.history)
            except Exception as e:
                error_text = str(e).strip()
                result.error = error_text if error_text else type(e).__name__
            finally:
                result.func_time = round(time.perf_counter() - start_2, 2)           
            result.AsyncClient_time = round(time.perf_counter() - start_1, 2)
        return result
    except asyncio.TimeoutError:
        result.error = f"TimeoutError: timed out after {timeout_func} seconds."
        return result


def table_print(results: list[LinkResult]):
    header_row = ROW_TEMPLATE.format(
            url="URL", status="Статус", final_url="Конечный URL", 
            redirects="Редиректы", error="Ошибка", 
            func_time="Время ф-ии", async_time="Время Async"
    )
    print(header_row)
    TOTAL_WIDTH = len(header_row)
    print("-" * TOTAL_WIDTH)
    for res in results:
        print(ROW_TEMPLATE.format(
            url=format_cell(res.url, W_URL),
            status=format_cell(res.status_code, W_STATUS),
            final_url=format_cell(res.final_url, W_FINAL_URL),
            redirects=format_cell(res.redirects, W_REDIRECTS),
            error=format_cell(res.error, W_ERROR, is_error=True),
            func_time=format_cell(res.func_time, W_FUNC_TIME),
            async_time=format_cell(res.AsyncClient_time, W_ASYNCCLIENT_TIME)
            ))


async def main():
    async with httpx.AsyncClient() as client:
        ask = await asyncio.gather(*(check_link(url, client) for url in get_urls_from_file(URL)))
        table_print(ask)

if __name__ == "__main__":
    asyncio.run(main())