import logging
import pandas as pd
import great_expectations as gx

logger = logging.getLogger(__name__)


def validate_cleaned_data(df: pd.DataFrame) -> bool:
    logger.info("Starting data validation with Great Expectations...")
    
    try:
        context = gx.get_context()
    
        datasource = context.data_sources.add_pandas("pandas_datasource")
        data_asset = datasource.add_dataframe_asset(name="cleaned_crypto_data")
        batch_definition = data_asset.add_batch_definition_whole_dataframe("batch_def")
        
        batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
        
        suite = gx.ExpectationSuite(name="crypto_quality_suite")
        
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="coin_id")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeGreaterThan(column="current_price", value=0)
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="market_cap")
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(column="symbol")
        )
    
        validator = context.get_validator(batch=batch, expectation_suite=suite)
        validation_result = validator.validate()
    
        if validation_result["success"]:
            logger.info("Data validation PASSED. All quality checks met.")
            return True
        else:
            logger.error(" Data validation FAILED!")
            for result in validation_result["results"]:
                if not result["success"]:
                    col = result['expectation_config']['kwargs'].get('column', 'unknown')
                    logger.error(f"  - Failed: {result['expectation_config']['type']} on column '{col}'")
            return False
            
    except Exception as e:
        logger.error(f"Validation process crashed: {e}")
        return False