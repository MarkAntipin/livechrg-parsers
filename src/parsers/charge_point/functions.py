"""Functions used for scraping https://driver.chargepoint.com"""


def make_params_string(params: dict) -> str:
    """Make the last part of the link to stations list"""
    res = str(params)
    res = res.replace("True", 'true')
    res = res.replace("False", 'false')
    res = res.replace("'", '"')
    res = res.replace(" ", "")
    return res
