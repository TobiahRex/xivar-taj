Black

1.
The snippet provides instructions for using a black box trading system, specifically for analyzing charts on different time frames (1m, 1h, and 15m) to determine trade triggers and exits. 

For the primary time frame (1m), the system suggests using the 5m chart to enter trades based on certain conditions, such as when prices close across the 5m 13ema (exponential moving average) or when there is momentum reflected through the histogram and RSIma (RSI moving average). If a 5m exit would result in a profit of less than 10p, the system advises ignoring the 5m exits and following the rules of Flag 8a. The trade protection and exit is determined by the 1h 13ema, unless another 1h exit presents itself.

For the 1h chart usage, the system recommends ignoring 5m buy triggers when the red ma cloud is present (8ema < 21ema), and ignoring 5m sell triggers when the blue ma cloud is present (8ema > 21ema). The RSIma momentum must support the 5m trade triggers, with the red line indicating sell triggers and the green line indicating buy triggers. The RSI histogram must be higher to buy and lower to sell, while the raw RSI must be up to buy and down to sell. Price must also close across the 13ema to support the trade.

For the 15m chart usage, the system advises ignoring this chart until after the first 1h exit in a trend. After the first 1h exit in the same trend, the system suggests substituting 15m trade confirmations for 1h.

Overall, the snippet provides guidelines for using different time frames and indicators to make trading decisions within the black box trading system.

2.
The snippet provides additional instructions and conditions for using the black box trading system, specifically regarding confirmations, entry and exit requirements, and the usage of the 15m chart.

1. Confirmations: Both entry and exit require confirmations.
2. 1h MA Cloud Color: The color of the 1h ma cloud still determines which trades to follow.
3. New 5m Entry Requirement: When the 15m chart is active, the 15m RSIma must cross 0 in favor of the trade. This requirement does not apply to the 1h chart in normal trading. The 15m chart still requires RSIma color, histogram, and raw RSI support for the 5m trade. 15m exits apply to both 15m RSI and 15m 13ema.
4. 1h RSIma Color: The 1h RSIma color may substitute for the 15m RSIma color as long as the 15m RSIma has crossed 0 in favor of the 5m entry trigger. The 1h RSIma color should never be fought against.
5. 1h Exit Triggers: 1h exit triggers are no longer relevant. The 1h acceleration flag or Flag 8a may interrupt 15m chart usage. Flag 8a may also override a 15m exit if it results in less than a 10p profit. If a 15m exit is less than 10p profit but the 1h 13ema supports the trade, the trade should be processed as if Flag 8a is active.
6. Disabling 15m Chart Usage: The 15m chart usage is disabled after the next 1h 8x21 MA crossover or if the 1h 21ema has turned against the 1h cloud or if the 1h RSIma crosses 0 against the cloud, whichever comes first. After the 15m chart is disabled, full 1h trade confirmation is required again.
7. 15m Exits: There are two 15m exits - the 15m RSI and the... (the snippet is cut off here)

These additional instructions provide more specific guidelines for using the black box trading system, including requirements for confirmations, entry triggers, exit triggers, and the usage of the 15m chart.

3.
The snippet provides additional instructions and scenarios for using the black box trading system, including the benefits of substituting the 15m chart and the trading flags.

1. Benefits of 15m Chart Substitution: Substituting the 15m chart offers several benefits, including not requiring the 1h histogram or RSIma color, faster entry and exit triggers with the same 5m entry triggers, maintaining the benefit of long-term confirmation of 5m triggers, and helping to avoid trade entry at long-term tops and bottoms.

To open the trading week:
1. Establish the long-term trend with the 1h MA cloud.
2. Await a 5m retrace regardless of whether a 5m trade trigger has presented itself.
3. After the 5m retrace, approach trading with the normal black box approach.
4. If the 1h cloud is blue and 5m prices are already below the 13ema, crossing above the 13ema does not constitute a retrace. Prices must move below the 13ema and then cross above again before a 5m buy trigger is executed, and vice versa.

Trading Flags:
1. Weekly Start Flag: Initialize the 1h trend for the 5m retrace requirement. The color of the 1h MA cloud determines the requirement for a 5m close crossing above or below the 13ema. Either condition clears the flag for normal trading.
2. Trading Range Flag: If the 1h rsi21ema is between 47-53 and has moved less than 1. 

These additional instructions and scenarios provide further guidance for using the black box trading system, including specific considerations for the 15m chart, opening the trading week, and trading flags.

4.
The snippet provides additional instructions and scenarios for using the black box trading system, including the trading range flag and the rules associated with it.

1. Trading Range Flag: If the 1h rsi21ema is between 47-53, the trading range flag is set. No trading signals should be executed in any time frame until the flag is reset. The flag is reset when the rsi21ema is above or below this range or when the raw RSI rises above 70 or below 30. 5m triggers should be ignored until a 5m retrace occurs. For example, if the 1h rsi21ema crosses above 53, the price must close below the 5m 13ema as a retrace, and vice versa. After the retrace, trading can resume normally.

2. Trading Range Exit: A trading range exit is treated as if it's a new 1h cloud color, except for the requirement of a 5m retrace. When exiting a trading range, a 5m retrace is required.

3. 1h rsi21ema Moves: The 1h rsi21ema may make moves greater than 1.8 from 2 bars ago inside the range of 47-53. This does not clear the flag. Only rising above 53 or dropping below 47, or the raw RSI, clears the flag. It's important to note that only 1 bar is required to establish the flag, and this may affect other bars that exceed 1.8 in movement inside the range.

4. Active Trade and Flag: If there is an active trade when the trading range flag is set, there are no special rules for exit. Exits should be processed normally as specified elsewhere.

These additional instructions and scenarios provide further guidance for using the black box trading system, specifically when the trading range flag is set. It introduces rules for trading signals, retraces, and exits when the market is in a trading range.

5.
The snippet provides additional instructions and scenarios for using the black box trading system, including the losing trade flag, RSI exit flag, and the 15m chart active flag.

1. Losing Trade Flag: The losing trade flag is set for ten 5m bars, indicating a no trading period where all triggers should be ignored. After the ten bars, the flag is cleared for normal trading. This helps avoid volatile whipsaws in the market.

2. RSI Exit Flag: The RSI exit flag is activated when the RSI is above 70 for 3 consecutive 1h bars in a blue cloud or below 30 for 3 consecutive bars in a red cloud. The histogram exit should be ignored as long as this flag is set. The flag should not disable flag 9, as it should remain active as long as the conditions for flag 9 are still met.

3. 15m Chart Active Flag: The 15m chart active flag is used as a simple toggle to determine whether to follow the 15m chart or the 1h chart. The flag is set after the first 1h exit (RSI, 13ema, 5ema, or histogram) in a trend. The flag is cleared when there is a 8x21 MA crossover (1h color change) or any other condition specified elsewhere.

These additional instructions and scenarios provide further guidance for using the black box trading system, including rules for no trading periods, RSI exits, and the usage of the 15m chart.

6.
The snippet provides additional instructions and scenarios for using the black box trading system, including the acceleration phase flag and the trading week start.

1. Acceleration Phase Flag: The acceleration phase flag is activated when prices close for 5 consecutive bars above the 1h 5ema in a 1h blue cloud or below the 1h 5ema in a 1h red cloud. This activates a 1h 5ema close to use instead of the 1h 13ema close. The 1h RSI close is still active, and a histogram exit is also implemented. The flag is reset when the 1h close is below (above) the 1h 5ema or when the 1h RSIma is no longer green in a blue cloud or red in a red cloud.

2. Trading Week Start: To start the trading week, the 5 bar count begins from the open on Sunday.

These additional instructions and scenarios provide further guidance for using the black box trading system, including rules for the acceleration phase and the start of the trading week.

7.
The snippet provides additional instructions and scenarios for using the black box trading system, including the modifications to the histogram exit.

1. Histogram Exit Modifications: The histogram exit may not capture the desired results when the market is trending but not strongly enough, reflected by candles that close against the trend. To mitigate this while not losing its many advantages, the following modifications are made:
   a. If a histogram close would result in less than a 10p profit, skip the close as long as the closing price has 1h 13ema support.
   b. If a 1h 5ema exit would result in less than a 10p profit, skip the close as long as the closing price has 1h 13ema support and the new close is 1h 13ema instead of 1h 5ema. This clears flags 8 and 9 as normal.
   c. Start a new histogram exit count (5 bars) from the bar following the bar that would have closed the trade.
   d. The valid exits during this whole time are 1h RSI and 1h 5ema (or 1h 13ema).
   e. A close across the 1h 5ema restarts the count and disables the 1h 5ema exit, activating the 1h 13ema exit again.
   f. After a 1h exit, the 15m chart will activate again normally.
   g. These modifications aim to improve the performance of the histogram exit and enhance the overall trading results.

These modifications help to refine the behavior of the histogram exit in different market conditions, ensuring that it is effective in capturing profitable trades while avoiding premature exits in trending markets.

8.
The snippet provides additional instructions and scenarios for using the black box trading system, including the histogram exit and the histogram exit flag.

1. Histogram Exit: The histogram exit is triggered after 5 closes above the 5ema in a blue cloud. When the histogram closes lower, the trade is exited at the close of that bar, even if the close is above the 5ema. After the exit, the next 5m buy trigger is taken if all 1h or 15m conditions are assumed to be true. If the 1h has not closed below the 5ema, Flag 8 is maintained even after an exit, while Flag 9 is reset. After 5 more closes above (below) the 5ema, Flag 9 is active again with the same rules. The new 5 bar count begins with the bar after the exit bar.

2. Histogram Exit Flag: The histogram exit flag is set after 5 closes above the 5ema in a blue cloud. While the histogram is down, the histogram exit is not active again until the histogram closes up. Only after the histogram closes up, the down histogram close becomes active again. The histogram being up or down is irrelevant when counting the 5 bars closing above the 1h 5ema. However, if the 6th histogram bar is down, the first bar after setting this flag will trigger the first histogram exit, regardless of whether the 5th histogram bar is up or down.

These additional instructions and scenarios provide further guidance for using the black box trading system, specifically for handling the histogram exit and managing the histogram exit flag. It allows for more precise trade exits based on the behavior of the histogram and ensures that the exit rules are followed consistently.

9.
The snippet provides additional instructions and scenarios for using the black box trading system, including the conditions for capturing the best exits, exceptions to Flag 9, and the Candlestick Suspend Trading Flag.

1. Best Exits Captured through Flag 11: Flag 9 captures the best exits when the 1h chart moves strongly. The conditions for capturing the best exits are reversed for a red cloud.

2. Exception to Flag 9 - Blue Cloud: In a 1h blue cloud, if the raw RSI is up on a histogram bar that is down and would otherwise trigger an exit, do not exit long trades. Maintain everything else as is and keep the histogram exit active. If the next histogram bar also signals an exit, do not exit if the raw RSI is up. The raw RSI must be down to exit a long trade using the histogram exit. The reverse conditions apply for a red cloud.

3. Exception to Flag 9 - Extreme RSI: When the 1h RSI is extreme for 3 consecutive bars in an active trade (less than 30 in a red cloud or greater than 70 in a blue cloud), ignore the Flag 9 exit (maintain the flag) and use the normal RSI exit (break across RSI 21ema or 30/70). Then process normally. The 15m chart will likely become active. This scenario is captured in Flag 5.

4. Candlestick Suspend Trading Flag: If a Shooting Star or Hammer pattern is present, stand aside for 3 additional bars if any of the following conditions occur:
   - Flag 8 is active.
   - Shooting Star is the highest high for 8 bars or Hammer is the lowest low for 8 bars.
   - Shooting Star has RSI greater than 70 or Hammer has RSI less than 30.

These additional instructions and scenarios provide further guidance for using the black box trading system, specifically for handling the best exits, exceptions to Flag 9, and the Candlestick Suspend Trading Flag. They help to refine the trading decisions based on specific market conditions and patterns, improving the overall performance of the system.

10.
The snippet provides additional instructions and scenarios for using the black box trading system, including the Histogram Reset Flag, 1h Trade Support Flag, and the Exit Methods.

1. Histogram Reset Flag: This flag is set when Flag 9 turns off and Flag 8 is still active. It activates new requirements for using Flag 9. The histogram exit is the bar moving against the current trade and cloud. This flag provides a simple way to monitor when to execute the histogram exit again. In a blue cloud, the flag is reset when the histogram moves up. In a red cloud, the flag is reset when the histogram moves down.

2. 1h Trade Support Flag: This flag is used to ignore 5m exits. It is set under the following conditions:
   - Blue 1h cloud: 1h buy trigger or (1h 21ema > previous bar and 1h RSIma > 0)
   - Red 1h cloud: 1h sell trigger or (1h 21ema < previous bar and 1h RSIma < 0)

3. Exit Methods:
   - Raw RSI > 70 for 3 bars and break lower below 70 or RSI 21ema, or
     RSI < 30 for 3 bars and break higher above 30 or RSI 21ema. Note that raw RSI may remain above 70 or below 30 for a considerable period, and we stay in the trade until the break across 70 or 30 or RSI 21ema.
   - Close across 13ema in any time frame.
   - Flag 8 exit.

These additional instructions and scenarios provide further guidance for using the black box trading system, specifically for handling the histogram reset, trade support, and different exit methods. They help to refine the trading decisions and provide more flexibility in managing trades based on specific conditions and scenarios.

11.
The snippet provides additional instructions and scenarios for using the black box trading system, including Flag 9 exit, 1h trade support, ignoring 5m exits, and specific rules for trading on Fridays.

1. Flag 9 Exit: The exit for Flag 9 is the 1h Histogram exit.

2. 1h Trade Support: When the 1h chart provides full trade support, ignore 5m exits. The 1h entry trigger always overrides 5m exit. If the 1h 21ema is trending with the trade and the 1h RSIma is across 0 supporting the trade, they override 5m exit. Note that the 1h close across 13ema is still the exit criteria in these types of trades. If the 1h 21ema is exactly equal to the previous bar, it provides trade support and is not against the trade.

3. Ignoring 5m Triggers: It is possible to get 5m triggers against the current trade when the 1h moving averages are supporting the trade. Ignore 5m triggers that contradict the current trade and do not exit. Use the normal 1h exit trigger to end the trade.

4. Obsolete.

5. Friday Exit Rules: On Fridays after 12 pm, execute the first exit trigger for any open trade unless Flag 8 is active or the 1h raw RSI is moving in favor of the trade or prices are above (below) the 1h 5ema and counting towards Flag 8 being active. Continue to follow Flags 8 and 9 and process normally, but do not open any new positions. Otherwise, exit all trades by 2 pm.

6. Friday Trade Prolongation: On Fridays after 12 pm, if a trade is being prolonged as outlined in #5, exit the trade if the 1h raw RSI moves against the trade.

7. Open no new trades after 9 am on Fridays.

These additional instructions and scenarios provide further guidance for using the black box trading system, particularly for handling 1h trade support, ignoring 5m exits, and implementing specific rules for trading on Fridays. They help to refine the trading decisions and provide more flexibility in managing trades based on specific conditions and scenarios.

12.
The snippet provides additional instructions for optimizing exit points and pips for a given trend using candlestick formations, specifically the shooting star and hammer patterns.

1. Candlestick Addition: The shooting star pattern applies to an uptrend with a blue cloud, and the hammer pattern applies to a downtrend with a red cloud. The gravestone and hanging top patterns are ignored as they are considered unreliable. These candle formations are used specifically for the shooting star in a downtrend and the hammer in an uptrend.

2. Candlestick Application: These candlestick patterns are applied on the 1h chart only. They can also work well on the 5m chart, but often it is desirable to stay in the trade as long as the trade has continued 1h support. If the shooting star or hammer pattern occurs while the 15m chart is active, the 1h exit is executed anyway. The 15m chart is ignored for the purpose of 15m shooting star/hammer patterns. If applicable, 15m exits are processed normally, assuming Flag 8 or 9 is not active, which disables 15m exits.

3. Exit with Acceleration Flag: If the acceleration Flag 8 is active and either the shooting star or hammer pattern appears, the trade will be exited at the close of that 1h bar instead of waiting for a 5ema cross, 13ema cross, histogram close, or raw RSI reverse move. This exit is always taken if the conditions are right.

These additional instructions provide guidance on using specific candlestick patterns, the shooting star and hammer, to optimize exit points in a given trend. They help to refine the exit strategy and provide more flexibility in capturing pips while considering the overall trend and market conditions.

13.
The snippet provides additional instructions and parameters for long-term backtesting of the trading system. It introduces new conditions and considerations to optimize the trading strategy.

1. Comparison of RSI34ema vs RSI21ema: The backtesting will involve comparing the current RSI value calculated using a 34-period exponential moving average (RSI34ema) with the current RSI value calculated using a 21-period exponential moving average (RSI21ema).

2. Comparison of Moving Averages: The backtesting will also involve comparing the current values of the 21-period exponential moving average (21ema), 34-period exponential moving average (34ema), and 55-period simple moving average (55sma).

3. Trading Range Definition: The trading range definition will be determined based on the amount of change from two bars ago. The current value is set to 2, but other values such as 1.8 can be tested to evaluate their effectiveness.

4. Entry Condition Variation: The backtesting will compare the requirement of closing prices crossing the 55sma for trade entry with not having this requirement.

5. Exit Condition Variation: The backtesting will compare the current exit condition of closing prices crossing RSI thresholds (70/30) for three periods with other variations such as 4, 5, or 2 periods.

6. Raw RSI Substitution: The backtesting will substitute the histogram entry confirmation on the 1h chart with the raw RSI value.

7. Mandated Raw 1h RSI for Trade Entry: The backtesting will consider mandating the use of the raw 1h RSI value for all trade entries.

These parameters provide additional flexibility and options for fine-tuning the trading strategy during the backtesting process. It allows for the evaluation of different variations and conditions to optimize the trading system's performance.

The snippet also raises questions about the backtesting process, such as whether one needs to relinquish their trading approach to backtest it and the potential risk of others stealing the profitable trading system once they see its performance. These questions highlight the considerations and challenges that may arise when conducting backtests and protecting one's trading strategies.

