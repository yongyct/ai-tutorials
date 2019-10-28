"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS


def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # limit leverage amount
    set_max_leverage(1.05)
    # Rebalance every day, 1 hour after market open.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_open(hours=1),
    )

    # Record tracking variables at the end of each day.
    algo.schedule_function(
        record_vars,
        algo.date_rules.every_day(),
        algo.time_rules.market_close(),
    )

    # Create our dynamic stock selector.
    algo.attach_pipeline(make_pipeline(), 'pipeline')
    
    context.ibm = sid(3766)
    context.amzn = sid(16841)
    context.spy = sid(8554)


def make_pipeline():
    """
    A function to create our dynamic stock selector (pipeline). Documentation
    on pipeline can be found here:
    https://www.quantopian.com/help#pipeline-title
    """

    # Base universe set to the QTradableStocksUS
    base_universe = QTradableStocksUS()

    # Factor of yesterday's close price.
    yesterday_close = USEquityPricing.close.latest

    pipe = Pipeline(
        columns={
            'close': yesterday_close,
        },
        screen=base_universe
    )
    return pipe


def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    context.output = algo.pipeline_output('pipeline')

    # These are the securities that we are interested in trading each day.
    context.security_list = context.output.index


def rebalance(context, data):
    """
    Execute orders according to our schedule_function() timing.
    """
    # if ratio > 1, leverage is used, dangerous
    # order_target_percent(context.amzn, 2)
    # order_target_percent(context.ibm, -2)
    order_target_percent(context.spy, 1)
    pass


def record_vars(context, data):
    """
    Plot variables at the end of each day.
    """
    record(amzn_close=data.current(context.amzn, 'close'))
    record(ibm_close=data.current(context.ibm, 'close'))
    record(leverage=context.account.leverage)  # leverage = gross exposure / net liquidation (~= equity)
    record(exposure=context.account.net_leverage)  # exposure = all outstanding positions, debt + equity. net leverage = net exposure / net liquidation
    pass


def handle_data(context, data):
    """
    Called every minute.
    """
    pass
