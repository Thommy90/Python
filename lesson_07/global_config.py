import logging

# Configure logging for debugging and tracking operations
logging.basicConfig(level=logging.INFO, format="{asctime} - {levelname} - {message}", style="{")

# Global configuration representing application settings
GLOBAL_CONFIG = {
    "feature_a": True,
    "feature_b": False,
    "max_retries": 3
}

class Configuration:
    def __init__(self, updates, validator=None):
        """Context manager for temporarily modifying the global configuration."""

        # Store the updates and the optional validator
        self.updates = updates
        self.validator = validator

        # To store the original state of the global configuration
        self.original_config = None

    def __enter__(self):
        """
        Enter the context: Apply the configuration updates.
        """

        self.original_config = GLOBAL_CONFIG.copy()
        logging.info(f"Original copy saved: {self.original_config}")

        try:
            GLOBAL_CONFIG.update(self.updates)
            logging.info(f"Attempting to apply updates: {GLOBAL_CONFIG}")
            if self.validator:
                self.validator(GLOBAL_CONFIG)
            logging.info(f"Updates applied: {GLOBAL_CONFIG}")
        except Exception as error1:
            self.__restore_config()
            raise ValueError (f"Validation or update failed: {error1}")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context: Restore the original configuration.
        """
        self.__restore_config()
        if exc_type:
            logging.error(f"Exception: {exc_value}", )
        return False

    def __restore_config(self):
        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self.original_config)
        logging.info(f"Configuratuion restored: {GLOBAL_CONFIG}")

    # Example validator function (Optional)
def validate_config(config: dict):
    """
    Example validator function to check the validity of the configuration.
    Ensures 'max_retries' is non-negative and 'feature_a' is a boolean.
    """
    if not isinstance(config.get("feature_a"), bool):
        raise ValueError("feature_a is not boolean.")
    if config.get("max_retries", 0) < 0:
        raise ValueError("max_retries can't be negative.")


# Example usage (for students to test once implemented)
if __name__ == "__main__":
    logging.info(f"Initial GLOBAL_CONFIG: {GLOBAL_CONFIG}")

    # Example 1: Successful configuration update
    try:
        with Configuration({"feature_a": False, "max_retries": 5}):
            logging.info(f"Inside context: {GLOBAL_CONFIG}")
    except Exception as error:
        logging.error(f"Error: {error}", )

    logging.info(f"After context: {GLOBAL_CONFIG}",)

    # Example 2: Configuration update with validation failure feature_a not boolean
    try:
        # to see how the context handles validation errors.
        with Configuration({"feature_a": "invalid_value", "max_retries": 3}, validator=validate_config):
            logging.info("This should not be printed if validation fails.")
    except Exception as error:
        logging.error(f"Caught exception: {error}")

    # Example 3: Configuration update with validation failure max_retries < 0
    try:
        # to see how the context handles validation errors.
        with Configuration({"feature_a": True, "max_retries": -1}, validator=validate_config):
            logging.info("This should not be printed if validation fails.")
    except Exception as error:
        logging.error(f"Caught exception: {error}")

    logging.info(f"After failed context: {GLOBAL_CONFIG}")
