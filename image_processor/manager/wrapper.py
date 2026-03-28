import logging

# Set up a logger to see errors in your Ubuntu terminal
logger = logging.getLogger(__name__)

class LambdaWrapper:
    def __init__(self, lambda_client):
        """
        :param lambda_client: The aioboto3 lambda client from your FastAPI app.
        """
        self.lambda_client = lambda_client

    async def create_fun(self, function_name, iam_role_arn, image_uri):
        """
        Rewritten to use Docker Images instead of ZIP files.
        """
        try:
            # We use PackageType='Image' to tell AWS to look at ECR
            response = await self.lambda_client.create_function(
                FunctionName=function_name,
                PackageType='Image',  # <--- Essential for Docker
                Role=iam_role_arn,
                Code={
                    'ImageUri': image_uri  # <--- The ECR URL of your worker container
                },
                Timeout=60,      # Processing images takes time
                MemorySize=512,  # Give Pillow enough RAM
                Publish=True
            )
            return response["FunctionArn"]
            
        except Exception as e:
            logger.error(f"Error creating Docker-based Lambda: {e}")
            raise
