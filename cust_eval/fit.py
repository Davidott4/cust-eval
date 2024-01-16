import logging

from lifetimes import GammaGammaFitter
from lifetimes import BetaGeoFitter


def fit_beta_geo(summary):
    """
    Fits the summary to BetaGeo and Gamma-Gamma models to build
    :param summary: summary generated from processing.build_summary_from_df
    :return: pandas.dataframe
    """

    # if we have customers with purchases <=0, then we do not have a poisson distribution
    summary = summary.reset_index()
    if summary[summary["monetary_value"] <= 0].shape[0] > 0:
        logging.warning("There are customers with 0-valued purchases, they will be removed")
    summary = summary[summary["monetary_value"] > 0]

    # measure correlation between frequency and monetary value
    correlation = list(summary[['frequency', "monetary_value"]].corr()["frequency"])[1]
    if correlation > 0.05:
        logging.warning("Purchase frequency and monetary value are correlated. This might reduce accuracy")

    # fit the BG/NBD model
    bgf = BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])

    # fit the Gamma-Gamma model
    ggf = GammaGammaFitter(penalizer_coef=0.0)
    ggf.fit(summary['frequency'], summary['monetary_value'])

    # predict customer lifetime value
    summary['num_predicted_purchases'] = bgf.predict(30, # assume 1 month
                                                 summary['frequency'],
                                                 summary['recency'],
                                                 summary['T'])
    summary['predicted_clv'] = ggf.customer_lifetime_value(bgf,
                                                           summary['frequency'],
                                                           summary['recency'],
                                                           summary['T'],
                                                           summary['monetary_value'],
                                                           time=1,
                                                           freq='D',
                                                           discount_rate=0.01)

    return summary


