import logging
from app.etl.orchestrator import ETLOrchestrator
from config import etl_config

logging.basicConfig(level=logging.INFO, filename='logs/etl.log', format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('etl-run')

def main():
    orchestrator = ETLOrchestrator(input_dir=etl_config.INPUT_DIR, output_dir=etl_config.OUTPUT_DIR, processed_dir=etl_config.PROCESSED_DIR, errors_dir=etl_config.ERRORS_DIR)
    result = orchestrator.run_players()
    logger.info(f'Result: {result}')
    print('ETL finished:', result)

if __name__ == '__main__':
    main()
