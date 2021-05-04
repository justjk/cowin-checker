# cowin-checker

**Cowin Checker** is a utility that allows you to check the status of available vaccination center in a district of your choice

## License
  - This utility is released under [MIT License](./LICENSE)

## Tech
  - This utility is built using Python 3.6 and [Scrapy](https://scrapy.org/)
  - The utility polls [Cowin website](https://www.cowin.gov.in/home) to see availability

## Env setup
  For local development
  - Setup virtual environment for this project using python3.6
  - Install dependencies mentioned in [requirements.txt](./requirements.txt) using pip3 in the created virtualenv
    ```
    $pip3 install -r requirements.txt
    ```
  - Install and enable [flake8](https://pypi.org/project/flake8/) linter
  - Install lib notify to enable desktop notifications on ubuntu. Execute the below command
    ```
    sudo apt-get install libnotify-bin
    ```

## Execution
  - From Cowin website, find the district_id for which you want to check. Use browser's Developer toolbar -> Network tab for this.
  - Inside the virtual environment, execute below command with your district_id to get the available centers. For example 307 is the district id for Ernakulam (Kerala)
        ```
        scrapy crawl cowin -a district_id=307
        ```
  - If centers with vaccine availability is present, you will get a notification.
  - Check the items.csv to get the center details, date and availability. If there are no centers with vaccines available, the items file will be empty
