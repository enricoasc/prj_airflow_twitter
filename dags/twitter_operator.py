import sys
sys.path.append("dags")

from airflow.models import BaseOperator, DAG, TaskInstance
from twitter_hook import TwitterHook
from datetime import datetime, timedelta
import json 
from os.path import join
from pathlib import Path

class TwitterOperator(BaseOperator):

    def __init__(self, file_path ,start_time, end_time, query ,**kwargs):
        self.start_time = start_time
        self.end_time = end_time
        self.query = query
        self.file_path = file_path
        super().__init__(**kwargs)
    
    def create_parent_folder(self):
        (Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)

    def execute(self, context):
        end_time = self.end_time
        start_time = self.start_time
        query = self.query
        
        self.create_parent_folder()

        with open(self.file_path,'w') as output_file:
            for pg in TwitterHook(end_time, start_time, query).run():
                # print(json.dumps( pg,indent=4,sort_keys=True))
                json.dump(pg, output_file, ensure_ascii=False )
                output_file.write('\n')

if __name__=="__main__":
    # MONTANDO URL
    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.00Z'

    end_time = (datetime.now() + timedelta( hours=3,seconds=-30) ).strftime(TIMESTAMP_FORMAT)
    start_time = (datetime.now() + timedelta(days=-90, hours=3 )).strftime(TIMESTAMP_FORMAT)
    query = 'datascience'

    with DAG(dag_id='TwitterTest',start_date=datetime.now()) as dag:
        to = TwitterOperator(file_path=join('datalake/twitter_datascience', f'extract_date={datetime.now().date()}', f'datascience_{datetime.now().date().strftime("%Y%m%d")}.json'), query=query, start_time=start_time, end_time=end_time, task_id='teste_run' )
        ti = TaskInstance(task=to)
        to.execute(ti.task_id)