from uuid import uuid4
import random


def generate_otp(uuid=uuid4()):
    """
    Generates a random OTP (One-Time Password) using UUID.

    Args:
        uuid (UUID): UUID object to generate OTP. Defaults to uuid4().

    Returns:
        str: The generated OTP.
    """
    return ''.join(random.sample(uuid.hex, 6)).upper()