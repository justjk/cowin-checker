# cowin-checker

**Cowin Checker** is a utility that allows you to check the status of available vaccination center in multiple districts of your choice at the same time. You can also filter based on age and get centers with availability that support your age group. Utility searches for dates upto 28 days from current date for availability.

On Ubuntu machines, you get a desktop notification if there is availability. List of locations are available as csv file.

## License
  - This utility is released under [MIT License](./LICENSE)

## Tech
  - This utility is built using Python 3.6 and [Scrapy](https://scrapy.org/)
  - The utility polls [Cowin website](https://www.cowin.gov.in/home) to see availability

## Env setup
  For local development
  - Setup virtual environment for this project using python3.6. I used [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) for easy setup.
  - Install dependencies mentioned in [requirements.txt](./requirements.txt) using pip3 in the created virtualenv
    ```
    $pip3 install -r requirements.txt
    ```
  - Install and enable [flake8](https://pypi.org/project/flake8/) linter
  - Install lib notify to enable desktop notifications on ubuntu. Execute the below command
    ```
    sudo apt-get install libnotify-bin
    ```
  - From Cowin website, find the district_id for which you want to check. Use browser's Developer toolbar -> Network tab for this.
  - Inside the virtual environment, execute below command with relevant district_ids (comma sperated) to get the available centers. For example 146 is the district id for North Delhi. 147 is for North East Delhi.
    ```
    scrapy crawl cowin -a district_id=146
    scrapy crawl cowin -a district_id=146,147
    ```
    If you want to filter by age, use the `age` flag as well as shown below. If age flag is set, centers where min age limit is <= age is considered.
    ```
    scrapy crawl cowin -a district_id=146,147 -a age=33
    ```
    
  - If centers with vaccine availability is present, you will get a notification (Ubuntu).
  - Check the items.csv to get the center details, date and availability. If there are no centers with vaccines available, the items file will be empty


## Cron Job setup
  - [Cron](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804) job can be setup to execute the utility at pre-defined intervals automatically
  - To setup a cron job, make modifications in `cronjob_entrypoint.sh` file as per your project settings and district/age requirements
  - You can edit your crontab with the following command:
    ```
    crontab -e
    ```
  - To set a job that runs every 2 minutes to check availability, set the below in the crontab editor -
    ```
    # replace with actual path to source code folder
    */2 * * * * bash ~/cowinchecker/cronjob_entrypoint.sh
    ```

## Dockerized execution (WIP - Notification not working)
  - Install docker client and daemon (Like duh!)
  - Checkout the code. cd into root directory of codebase. Build docker image
    ```
    cd cowinchecker
    docker build -t cowinchecker:latest .
    ```
  - From Cowin website, find the district_ids for which you want to check. Use browser's Developer toolbar -> Network tab for this.
  - Run docker container and pass district id as argument. For example 146 is the district id for North Delhi. 147 is for North East Delhi.
    ```
    docker run cowinchecker:latest 146
    docker run cowinchecker:latest 146,147
    ```
    If you want to filter by age, pass age as second parameter (optional). If passed, centers where min age limit is <= age is considered.
    ```
    docker run cowinchecker:latest 146,147 33
    ```