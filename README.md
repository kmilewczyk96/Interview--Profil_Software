># Web Crawler:
>Author: Karol Milewczyk
>
>### Preparing dependencies:
>
>1) Install virtual environment in project's directory.
>2) With your venv activated, run `pip install -r requirements.txt`
>
>## How to run:
>
>>### Crawler:
>>ex. `python -m app crawl --page https://example.com/ --format csv --output /home/User/example`
>>1) Page param is required.
>>2) Format param is optional, you can choose between json and csv, where json is set by default.
>>3) Output format is optional, by default it is set to: *your current directory*/output
>><br>NOTE: the script won't create directories for you, and output MUST be an absolute path.
> 
>>### Print-tree:
>>ex. `python -m app print-tree --page https://example.com/`
>>1) Page param is required. It is also the only param available.
>
>>### Tests:
>>simply: `pytest`
> 
> ## Additional notes:
> 
> 1) By default, script limits requests to 30 per second, you can change it by changing `Model`param in `app/__main__.py`
