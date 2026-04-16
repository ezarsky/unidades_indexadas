# Uruguayan Mortgages or: How Your Loan Gets Worse Before It Gets Better 

## The Situation

So a couple of weeks ago, my girlfriend asked me for help with figuring out how much money she owed on her mortgage. Though I'm no banker by any stretch, I thought it could be a great excuse to play around in Excel, so I agreed to take a look. She showed me the mortgage statement, and, in addition to lots of new Spanish finance jargon to parse (*TEA*, *saldo capital*, *complementos cuota*), I was surprised to see a currency (*moneda*) I hadn't encountered before: **UI**. 

I asked her what this was, and she said it had something to do with inflation, but she wasn't sure. It was time for some digging. Get ready for a boatload of acronyms.

## What Are UI?

A bit of Googling revealed a few basics pretty quickly:
- *UI* stands for *unidad(es) indexada* or "indexed unit(s)". So UI are an index of something, and as my girlfriend mentioned before, it probably indexes inflation, so it's a way to measure rising prices.
- Each UI is worth a certain number of Uruguayan pesos (UYU) on any given date. For example, on March 13, 2020 (the day when the first COVID cases were reported in Uruguay), 1 UI was valued at 4.4662 pesos, or, put another way, 10,000 UI were valued at 44,662 pesos. 
- The Uruguayan government has published UI values each month for more than 20 years, and there are values going all the way back to June 1, 2002, which is when 1 UI was valued at 1 peso. 
- When the government publishes the UI values for a given month, the values start at the 6th of that month and continue into the future up to the 5th of the following month. For example, in April 2026, the National Statistics Institute (INE) published a table of UI values for every date from April 6, 2026, to May 5, 2026.

So the goverment determines how much each UI is worth a little bit ahead of time: on November 14, 2028, you will already be able to look up the value of 1 UI up to December 5, 2028. But how does the government come up with these values? A lot of the sources had little to say about this, but the *informes técnicos* (technical reports) from INE provide a [table of values for a given month followed by notes on their methodology](https://www5.ine.gub.uy/documents/Estad%C3%ADsticasecon%C3%B3micas/PDF/UI/2025/UI%20Mayo%202025.pdf). The notes reveal that the UI was created as a result of [Law No. 17.761](https://archivo.presidencia.gub.uy/ley/2004051303.htm), which 

1. sets the initial value of 1 UI at 1.2841 pesos on August 1, 2003, and
2. defines how the sequence of values will be calculated henceforth

among a few other details that aren't important for our purposes. The law specifies that there are two formulas for calculating the value of 1 UI in pesos. Here's what the law says:

- For the first 5 days of month $M$ (i.e., for $1\le d \le 5$), the value of 1 UI on day $d$ is given by
$$UI_{d, M}=UI_{5, M-1}\left(\frac{IPC_{M-2}}{IPC_{M-3}} \right)^{\frac{d+D_{M-1}-5}{D_{M-1}}} $$

- For the remaining days of the month (i.e., for $6\le d \le 31$), the value of 1 UI on day $d$ is given by
$$UI_{d, M}=UI_{5, M}\left(\frac{IPC_{M-1}}{IPC_{M-2}} \right)^{\frac{d-5}{D_{M}}} $$

Thorny stuff, but it's less thorny than it would seem at first glance. If you don't want to dig in, [feel free to skip](#how-do-ui-relate-to-mortgages) a not-very-quick technical diversion. Otherwise, we're going to try to reconstruct these two formulas intuitively.

## How Are UI Calculated?

### Monthly Inflation
We'll start by tackling what UI are fundamentally measuring: inflation. How does the government measure inflation? Since [inflation](https://en.wikipedia.org/wiki/Inflation) is the increase in average price for goods and services, a sensible way to measure inflation would be to collect prices for a bunch (or *basket*) of goods and services on some day, then prices for the same bunch (*basket*) of goods and services on another day, and calculated how much the price of the bunch (*basket*) changed. 

This is a whole topic in itself, so we won't dig in too much here, but here's a small, simplified example. Let's say we define the basket of goods and services to be 1 apple and 1 banana. If yesterday 1 apple cost 30 pesos and 1 banana cost 20 pesos, and today 1 apple costs 35 pesos and 1 banana costs 24 pesos, then 

- the price of the basket yesterday is $30+20=50$ pesos, 
- the price of the basket today is $35+24=59$ pesos, and
- the price of the basket increased by $59-50=9$ pesos.

If we stop here and say inflation was 9 pesos from yesterday to today, a question might arise: is 9 pesos a big change or a small change? To answer this, it's helpful to compare this increase to something else, and we usually use the earlier price as a point of comparison, in this case 50 pesos. 9 pesos is a certain proportion of 50 pesos:

$$ \frac{59-50}{50} = \frac{9}{50} = 0.18 = 18\% $$

so we might say that there was an 18% inflation in prices from yesterday to today or that the *rate of inflation* from yesterday to today was 18%. One important note about this calculation is that we could get this value a bit faster by dividing the price today by the price tomorrow:

$$ \frac{59}{50} = 1.18 = 118\% $$

We can interpret this a few ways.

1. If we define the price yesterday as 100%, the price today is 118%, so the price today is higher, and it's higher by 18% of the price yesterday.
2. We can multiply the price yesterday by 1.18 to get the price today. This 1.18 can be called the *inflation factor* from yesterday to today.

In essence, that's what the government does to measure inflation. At some point in the past, they define a basket of goods and services, and they measure how the price of that basket changes from one month to the next. Ignoring some technical details, that final "price of the basket" in Uruguay in a given month is called the **IPC** or *índice de precios del consumo*.

If they want to measure inflation from one month to another, they can do exactly what we did earlier. Let's say that $IPC_{Feb}$ is the IPC (basket price) for February 2026 and $IPC_{Mar}$ is the IPC (basket price) for March 2026. To find out how much inflation there was between February and March, we can either

- find the difference in basket prices and divide the result by the basket price for February
    $$ \frac{IPC_{Mar} - IPC_{Feb}}{IPC_{Feb}} = r\% $$
    which gives us the rate of inflation $r$, or

- divide the basket price for March by the basket price for February
    $$ \frac{IPC_{Mar}}{IPC_{Feb}} = b $$
    which gives us the inflation factor $b$.

It might help us understand this more clearly if we use some made-up numbers. Let's say that $IPC_{Feb} = 20$ and $IPC_{Mar} = 21$. Then the inflation rate $r$ is
$$ \frac{21-20}{20} = \frac{1}{20} = 0.05 = 5\% $$
and the inflation factor $b$ is
$$ \frac{21}{20} = 1.05 = 105\%$$

### Daily Inflation

The basket of goods and services we used earlier that had just 1 apple and 1 banana is very simplistic. In reality, when INE defined the basket of goods and services, they considered thousands of different products and services that people might buy on a regular basis, from foods to electronics, from healthcare to transportation. INE collects these prices once per month, but the prices for some goods or services can change from one hour to the next, so it seems unrealistic to act like prices stay frozen in place for all of February and then suddenly jump up in March. So how does the government measure inflation—price changes that might happen on an hourly basis—if they only collect prices once per month?

The answer is they don't. It's probably hard enough to collect prices for all of these goods and services across the whole country every month; it's practically impossible to do so every hour or even every day. Instead, they assume that inflation happens smoothly, at approximately the same pace every day.

To see how this works mathematically, let's look back at our simplified example of a basket of goods where the basket price yesterday was 50 pesos and the inflation rate was 0.18 or 18% per day. The inflation factor in that example was 1.18 or 118% each day. Notice that we can subtract 1 from the inflation factor to get the inflation rate: $1.18-1=0.18$. Another way to say this is we can subtract 100% from the inflation factor to get the inflation rate: $ 118 \% - 100 \% = 18 \% $. This is important because we often hear an inflation rate reported, like in a news report that says, "Inflation was 3.8 \% last year," but the inflation factor is probably more useful for calculating new price levels. 

For example, let's say that yesterday's basket price is 50 pesos, and that inflation is 18% per day every day. Then today (1 day after yesterday), the basket price will be
$$50(1.18) = 59$$
in other words, the price started at 50 pesos and was inflated *one time* by a factor of 1.18.

Tomorrow (2 days after yesterday), the basket price will be
$$50(1.18)(1.18) = 69.62$$
A shorter way to write this is
$$50(1.18)^2 = 69.62$$
in other words, the price started at 50 pesos and was inflated *two times* by a factor of 1.18. 

The day after tomorrow (3 days after yesterday), the basket price will be
$$50(1.18)(1.18)(1.18) = 82.1516$$
or
$$50(1.18)^3 = 82.1516$$
in other words, the price started at 50 pesos and was inflated *three times* by a factor of 1.18.

Perhaps you see a pattern here. If we want to know the price $d$ days after yesterday, it can be found by starting at 50 pesos and inflating the price *$d$ times* by a factor of 1.18
$$50(1.18)^d = y$$
where $y$ is the price $d$ days after yesterday.

In general, if we start with a price $a$ and the inflation factor every day is $b$, then the price $y$ after $d$ days of inflation is

$$y=a(b)^d$$

Why is all of this important? Let's continue the example of inflation from February 2026 to March 2026, and let's assume that prices are collected and IPC values are calculated on the 1st of each month. Say we want to estimate *daily* inflation (which we're assuming is the same every day) over the month of February. The starting price $a$ is $IPC_{Feb}$, and the ending price $y$ is $IPC_{Mar}$. If $b$ is the daily inflation factor, we have

$$IPC_{Mar} = IPC_{Feb}(b)^D$$

where $D$ is the number of days in February. Since there were $D=28$ days in February 2026 (February 1st to March 1st), we can say that

$$IPC_{Mar} = IPC_{Feb}(b)^{28}$$

in other words, the basket price started at $IPC_{Feb}$ and was inflated 28 times by a factor of $b$ to arrive at a basket price of $IPC_{Mar}$. What we're trying to find is $b$, some constant daily inflation factor that would explain the price increase from February to March. If we isolate $b$ in this equation, we'll have a way to calculate this $b$ from the montly basket prices.

First we can divide both sides of the equation by $IPC_{Feb}$, which gives us

$$\frac{IPC_{Mar}}{IPC_{Feb}} = (b)^{28}$$

This equation has a real-world meaning: the monthly inflation factor $\frac{IPC_{Mar}}{IPC_{Feb}}$ is the same the daily inflation factor $b$ applied 28 times.

To solve for $b$, we can do the 28th root of each side, which gives
$$\sqrt[28]{\frac{IPC_{Mar}}{IPC_{Feb}}} = b$$
which is kind of ugly. Alterntatively, doing the 28th root of each side is the same as raising each side to the $\frac{1}{28}$ power:
$$\left( \frac{IPC_{Mar}}{IPC_{Feb}} \right)^{\frac{1}{28}} = b$$

Either of these is correct, and they mean the same thing: $b$ is the inflation factor you would apply 28 times to get the monthly inflation from February to March. Let's use the made-up numbers we used earlier to make this a bit more concrete. If $IPC_{Feb} = 20$ and $IPC_{Mar} = 21$, then we already calculated the monthly inflation factor to be 

$$\frac{21}{20} = 1.05 = 105 \% $$

If the daily inflation factor is in fact the same every day of the month of February, then it equals
$$\left( \frac{21}{20} \right)^{\frac{1}{28}} = \left( 1.05 \right)^{\frac{1}{28}} \approx 1.0017 =100.17 \%= b$$
so in this example, the monthly inflation rate was 5% from February to March, and the daily inflation rate was about 0.17%, so prices rose by about 0.17% on average every day. Cool.

Getting back to INE's formulas: instead of giving the months names like February or July, they give each month a number, like 7 or 39. Since the UI had its initial value established for August 2023, you might call that month 1, though it doesn't really matter what number it's given as long as it's an integer. If you know the basket price $IPC_{M}$ for some month $M$, the basket price $IPC_{M-1}$ for the month before it $M-1$, and the number of days $D_{M-1}$ in the month before it, then we can estimate the daily inflation factor $b_{M-1}$ for the previous month as
$$ b_{M-1} = \left( \frac{IPC_M}{IPC_{M-1}} \right)^{\frac{1}{D_{M-1}}} $$

which looks a lot like some parts of the formulas in [Law No. 17.761](https://archivo.presidencia.gub.uy/ley/2004051303.htm).

### Estimating Mid-Month Prices: UI

So far we've seen that there's a way—albeit an imperfect one—to measure inflation on a monthly basis and a way to use monthly inflation to estimate daily inflation. But wait, what does all of this have to do with mortgages? Why should all this monthly and daily price change stuff matter if I'm just borrowing money to pay for my house?

One short way to answer this question would be to say that mortgages are loans that last quite a long time, usually at least 10 years and often lasting for 30 years. Over that time, prices in general are going to increase pretty significantly, which means the bank's expenses are going to increase pretty significantly (they buy goods and services, too). For example, if the rate of inflation is a modest 2% per year, then something that cost the bank 1,000 pesos in the first year of your loan will likely cost around $1000(1.02)^30 \approx 1811.36$ pesos by the end of the loan, nearly double what it was at the start. And often the rate of inflation is quite a bit higher than 2%. If instead the rate was 5% per year, that same item would likely cost around $1000(1.05)^30 \approx 4321.94$, more than 4 times the amount it cost at the start. Banks aren't usually interested in losing money, so they're going to adjust your mortgage payments according to the current rate of inflation to ensure that inflation doesn't bleed them dry.

 That's all well and good, but another question remains: why would daily inflation matter instead of just monthly or yearly inflation? To answer that, let's imagine you're a running a bank like BHU, and inflation is roaring right now. Let's say the rate of inflation is something crazy like 10% per month, so the inflation factor each month is 1.1. In a 30-day month, this would correspond to a daily inflation factor of $(1.1)^{\frac{1}{30}} \approx 1.0032$, so a daily inflation rate of about 0.32%. Doesn't sound that bad. However, let's say that you have two clients who owe you 10,000 pesos this month: Client A pays on the 10th of the month, and Client B pays on the 20th of the month. Over the 10 days between when Client A pays and when Client B pays, prices in general are expected to increase by a factor of approximately $(1.1)^{\frac{10}{30}} \approx 1.032$, or by about 3.2%. 

What this means for you is that the money you receive from Client B is worth somewhat less than the money you receive from Client A. To illustrate, let's say you also have to pay for office supplies twice per month: once on the 10th and once on the 20th. Let's say on the 10th that those supplies cost 10,000 pesos. What luck! The payment from Client A will cover that expense perfectly. However, since prices are generally rising by about 3.2% every 10 days, it wouldn't be unreasonable to find that on the 20th those same supplies now cost 3.2% more, or 10,320 pesos. Uh-oh. Client B's payment doesn't cover the costs of the supplies, and the only reason for this is that prices are rising pretty quickly. You can imagine that banks want to avoid this situation. Indeed, they decided it's best to inflate the payments they ask from clients so that they can guarantee that inflation won't undermine their ability to cover their costs and/or make a profit. And thus was born our friend the "indexed unit" or UI.

As mentioned earlier, [Law No. 17.761](https://archivo.presidencia.gub.uy/ley/2004051303.htm) established the value of 1 UI at 1.2841 pesos for August 1st, 2003. From that point on (ignoring some minor technical details about the calculation for the rest of August 2003), the UI has been increased on a daily basis according to monthly inflation estimates from the government. To illustrate how this works, let's go back to the made-up numbers we used for monthly inflation earlier. As a reminder, we imagined that the basket price for February was $IPC_{Feb} = 20$ and for March was $IPC_{Mar} = 21$. We calculated the monthly inflation factor to be 

$$ \frac{21}{20} = 1.05 = 105 \% $$

and the estimated daily inflation factor for every day of the month of February as

$$ \left( \frac{21}{20} \right)^{\frac{1}{28}} = \left( 1.05 \right)^{\frac{1}{28}} \approx 1.0017 =100.17 \%= b $$

Let's now say that on March 1st, 2026, 1 UI is equal to 5 pesos. Then if we make the assumption that daily inflation is going to continue the same way it did last month (which seems pretty reasonable), we can calculate the UI values for the rest of the month so that they follow that inflation. On March 2nd (1 day after March 1st), 1 UI should be valued at

$$ 5(1.0017) = 5.0085 $$

pesos. On March 3rd (2 days after March 2nd), 1 UI should be valued at

$$ 5(1.0017)^2 = 5.017 $$

pesos.On March 4th (3 days after March 2nd), 1 UI should be valued at

$$ 5(1.0017)^3 = 5.0255 $$

pesos. You might notice a very similar pattern to one we saw earlier. For a day in March 2026 that is $d$ days after March 1st, 1 UI should be valued at

$$ 5(1.0017)^d $$

pesos. Since 1.0017 is the same as $\left( \frac{21}{20} \right)^{\frac{1}{28}}$, we might instead write this as

$$ 5 \left( \left( \frac{21}{20} \right)^{\frac{1}{28}} \right)^d $$

or simplifying using the laws of exponents

$$ 5 \left( \frac{21}{20} \right)^{\frac{d}{28}} $$

More generally, if we know the basket price $IPC_{M}$ for some month $M$, the basket price $IPC_{M-1}$ for the month before it $M-1$, the UI value $UI_{0, M}$ on the 1st day of month $M$, and the number of days $D_{M-1}$ in the month before it, then we can calculate $UI_{d, M}$, the UI value $d$ days after the  1st day of month $M$, as

$$ UI_{d, M} = UI_{0, M} \left( \frac{IPC_M}{IPC_{M-1}} \right)^{\frac{d}{D_{M-1}}} $$

which is looking dangerously close to what we see in the formulas given in [Law No. 17.761](https://archivo.presidencia.gub.uy/ley/2004051303.htm).



### Back to the UI Formulas
The final formula above isn't the same as what's in the law, though. That's because what we described here isn't exactly what INE does. Let's break it down:

- To calculate the UI for a given month, INE doesn't use the "basket prices" (IPCs) for that month and the previous month to estimate monthly inflation. Instead, they use the IPCs for the two previous months. For example, to calculate a monthly inflation factor to use in the September UI calculations, INE will use the IPC for August and the IPC for July. It's easy to imagine that the price collection and IPC calculation process is lengthy and cumbersome, so they probably do this to avoid, for example, having to wait on September's IPC data to calculate September's UI values. It may also be that the IPC for a given month is published relatively late in the month, which would mean that IPC isn't available to calculate that month's UI values. Here's how this changes our formula above:
    $$ UI_{d,M} = UI_{0,M} \left( \frac{IPC_{M-1}}{IPC_{M-2}} \right)^{\frac{d}{D_{M-1}}} $$

- INE uses the inflation from two months ago up to one month ago as its estimate of monthly inflation for this month, but they don't estimate daily inflation between two months ago and one month ago. Instead, they assume that monthly inflation will continue over *this month*, and they find daily inflation estimates for *this month*. For example, INE uses the IPC for August and the IPC for July to calculate UI values for September, but they don't break up the resulting monthly inflation factor into 31 parts (31 days between July measurement of IPC and August measurement of IPC). Instead, they break up the monthly inflation factor into 30 parts, since there are 30 days in September. It's a bit odd because the July-to-August inflation happened over 31 days, not over 30, but to me it seems like they're assuming *monthly* inflation will be the same over the month of September, and they break that up into 30 *daily* inflation factors to reflect that assumption. It probably doesn't make a big difference in the long run, and it's probably as good of an assumption as any other they might have made instead. Anyway, here's how this changes our formula above:
    $$ UI_{d,M} = UI_{0,M} \left( \frac{IPC_{M-1}}{IPC_{M-2}} \right)^{\frac{d}{D_{M}}} $$

- INE chooses the 5th day of the month as the starting point for the calculation. I'm not entirely sure why, but presumably sometime on or before the 5th of a certain month, we will have the $IPC$ value for the previous month and we can calculate all the $UI$ forward up to and including the 5th of the following month. For example, on or before September 5th, we should have the $IPC$ value for August and the one for July, and we can calculate all the daily $UI$ values for September.  Perhaps 5 was chosen to account for the possibility of weekends at the start of the month, holidays, etc.

    It's important to note that this means that if you want to refer to the date $d$ of the month, that date will be $d-5$ days after the 5th of the month. For example, September 6th ($d=6$) is $6-5=1$ day after September 5th. September 24th ($d=24$) is $24-5 = 19$ days after September 5th. Here's how this changes our formula above: for any date $d$ in month $M$ after $d=5$
        $$ UI_{d,M} = UI_{5,M} \left( \frac{IPC_{M-1}}{IPC_{M-2}} \right)^{\frac{d-5}{D_{M}}} $$

- Choosing the 5th day of the month as the starting point has two other important implications:

    1. that we need to continue the UI calculations for a given month into the following month until we reach the 5th day of that month, and
    2. that the UI values up to the 5th of the month need to have been done when the previous month's UI values were calculated.
    
    The first implication says that days 1 through 5 of next month will use the same formula. This shouldn't be a problem. For example, September 30th ($d=30$, the last day of September) is $30-5=25$ days after September 5th. The next day is October 1st, which is $31-5 = 26$ days after September 5th. It might be a little tricky, but one way we can get this consistently correct is to imagine that these 5 days of the next month are like a continuation of this month. In this example, we could view October 1st as "September 31st", October 2nd as "September 32nd", and so on until October 5th is like "September 35th". It's not literally true, but it's a useful fiction. Mathematically, what we just did is the same as adding the next month's date $d$ to the number of days in this month $D_M$, so October 3rd is like "September 33rd" since $30+3 = 33$. Here's how this changes our formula above: for any date $d$ in month $M+1$ up to and including $d=5$
        $$ UI_{d,M+1} = UI_{5,M} \left( \frac{IPC_{M-1}}{IPC_{M-2}} \right)^{\frac{D_{M}+d-5}{D_{M}}} $$

    The second implication is essentially taken care of by the first; we just need to change our perpective a bit. Everything we said above about "this month" and "next month" also apply if we replace "this month" with "last month" and "next month" with "this month". Using the example above, instead of IPCs for July and August to calculate UI values in September and early October, we would have IPCs for June and July to calculate UI values in August and early September. Mathematically, in the formula above, we would move every month back by 1, so 
    - $M-2$ becomes $M-3$
    - $M-1$ becomes $M-2$
    - $M$ becomes $M-1$
    - $M+1$ becomes $M$
    and the formula for the first 5 days of month $M$ is
    $$ UI_{d,M} = UI_{5,M-1} \left( \frac{IPC_{M-2}}{IPC_{M-3}} \right)^{\frac{D_{M-1}+d-5}{D_{M-1}}} $$

And there we have it! That's how INE calculated the value of 1 UI every month: 
- For the first five days of month $M$:
    $$ UI_{d,M} = UI_{5,M-1} \left( \frac{IPC_{M-2}}{IPC_{M-3}} \right)^{\frac{D_{M-1}+d-5}{D_{M-1}}} $$

- For the rest of the month:
        $$ UI_{d,M} = UI_{5,M} \left( \frac{IPC_{M-1}}{IPC_{M-2}} \right)^{\frac{d-5}{D_{M}}} $$

(Side note: I'm still not exactly sure what prompted the creation of the UI. My suspicion is that it was created as a way to protect Uruguayan financial institutions in the wake of the [Uruguayan banking crisis of 2002](https://en.wikipedia.org/wiki/2002_Uruguay_banking_crisis), which itself seems to have been due largely to Argentinian and Brazilian economic woes around the same time. However, this is pure guesswork on my part. Perhaps a better informed and more economically-sophisticated reader can provide clarity/correction.)

Now we know that the IPC is one way the government measures inflation and that the UI is an estimate of daily inflation. Or we might think of it as a new currency that doesn't inflate: something that costs 30 UI should more or less always cost 30 UI, because when prices in pesos increase, that triggers a corresponding increase in the value of 1 UI in pesos. Either way, banks probably feel a lot safer offering you a 15-year, 20-year, or 30-year loan in UI than they would offering the same loan in pesos because the payments you make will be adjusted for inflation, so the banks should be essentially immune to rising prices.


## How Do UI Relate to Mortgages?

As mentioned in the side note above, the UI probably serves to shield Uruguayan financial institutions from the effects of inflation, though this means they simply pass the buck on to their consumers: the population, AKA the people, AKA the common folk. A simplified example can help illustrate.

Let's say that on January 1st, 2010, you wanted to buy a house in Uruguay, and you needed to borrow 100,000 USD (prices for big ticket items like houses, cars, and major appliances are usually given in USD instead of UYU). Say you had gone to the Mortgage Bank of Uruguay (el *Banco Hipotecario de Uruguay* or BHU) for the loan, and that, after much bureaucratic paper-pushing, they approved your application. Then you would have received a loan for around 967,113.15 UI. 

Wait, what? Weren't you supposed to be getting a loan for 100,000 USD? Well, sort of: they wouldn't give you the loan in USD (or UYU for that matter), because that would expose them to inflation. Plus, it's not the national currency of Uruguay, and the Uruguayan government has little conrol over USD. Instead:

- The bank would have converted 100,000 USD to around 1,935,000 UYU (the exchange rate on January 1st, 2010, was 19.35 UYU to 1 USD).

- Then they would have converted the 1,935,000 UYU to around 967,113.15 UI (the exchange rate on January 1st, 2010, was 2.0008 UYU for 1 UY).

Let's say you went for a 15-year fixed-rate mortgage with a 6% annual interest rate (not unreasonable). The three graphs below show for each month

- the remaining balance on the loan, 
- the total amount you had paid up to that point,
- the total amount you had paid against the principal up to that point,
- the total extra amount you had paid due to interest up to that point, and
- the total extra amount you had paid due to inflation up to that point.

![15-Year Mortgage Numbers for UI (Indexed Units)](./ui_mortgage_nums.png)

The first graph shows all these values in UI. A few features to note:
1. Your remaining balance (blue) steadily declines, slowly at first and more quickly the farther you are into the loan.
2. The total amount paid against principal starts at zero and increases until it reaches exactly the amount you originally borrowed.
3. The total extra amount paid due to interest starts at zero and grows faster than the amount of principal paid, but eventually levels off.
4. The total cost (total amount paid) ends up much higher than the amount you borrowed. In the case of UI, this is entirely due to interest: all the extra amount you pay back above what you borrowed is due to interest.
5. In the case of UI, there is no cost due to inflation. If you could somehow earn money and pay the loan entirely in UI, inflation would have no impact on your loan since your income and payments would already be adjusted to account for inflation.

Now let's look another graph of the same loan but in terms UYU, since that's the currency in which most Uruguayans would actually be earning income and making payments:

![15-Year Mortgage Numbers for UYU (Uruguayan Pesos)](./uyu_mortgage_nums.png)

The graph looks pretty similar to the graph for UI, but with a few important differences:
1. Your remaining balance in UYU actually *increases* at first (in this case, but not in every case) for 5 or 6 years before starting to diminish. It was precisely this feature that surprised me when I first started investigating this topic, since it went so contrary to my intuition. How could you possibly pay the bank for several *years* and somehow owe even more money to them than you did at the start? The answer, of course, is that you owe more UYU than you did at the start, but not more UI. Even though your balance is technically always decreasing in UI, this scheme has some practical consequences for the people paying the mortgage. When I eventually worked out what was going on and showed my girlfriend what the situation was, she was more than a little miffed. She had been paying the bank steadily for 5 years, and yet she owed more money to them than she had originally borrowed (in UYU). Not a fun realization.
2. The total amount paid against principal and the total extra amount paid due to interest function very similarly to how they did for UI.
3. The total cost of the loan is again higher than the amount borrowed, but much more so than in the UI case. There culprit here is inflation: the total extra amount paid due to inflation starts at zero, but as time goes on, inflation becomes a bigger and bigger part of what you pay, in this case eventually exceeding both total principal paid and total interest paid.

An interesting final exercise might be to look at the same loan but imagine that you earn money in USD and that you exchange USD for UYU each month to make the payments:

![15-Year Mortgage Numbers for USD (US Dollars)](./usd_mortgage_nums.png)

Again there are some commonalities with the other two graphs, but some differences are even more stark:
1. Your remaining balance in USD also increases at first (though it doesn't have to), but it's very unstable, with some sharp increases and decreases over the 15 years of the loan. This is in part due to inflation in Uruguay, but the instability is mostly due to the exchange rate between UYU and USD. Sometimes each dollar of yours will buy you 32 pesos, other times 18 pesos, and still others 43 pesos.  
2. That same instability appears in the total cost, principal paid, interest paid, and inflation paid curves. You eventually end up paying exactly the 100,000 USD that you borrowed, but there are a lot of extra USD thrown around to cover interest and inflation, and those numbers get shifted around each month as the exchange rate between UYU and USD fluctuates.

The big takeaway from these three graphs is this: in technical terms, you're always decreasing the amount you owe on a mortgage when you make payments, but in practical terms, you may spend several years making payments but steadily owing more than you borrowed. From conversations with other Uruguayans, it seems like this isn't exactly common knowledge, and people seem to accept that their payments (*cuotas*) in pesos are increasing little by little each month. Perhaps this is because salaries also get adjusted twice per year to account for inflation. I don't know if the salary adjustment exactly compensates for the mortgage payment adjustments or not, but that'll have to be a topic for another time.

## Mortgage Payments Over Time

Speaking of payment adjustments, let's take a closer look at the monthly payments for that 15-year loan. Some part of each payment goes toward paying off interest that has accrued over the month, and another part goes toward paying off the principal. The payments in a typical mortgage are calculated to be the same amount every month, so no part of the payment compensates for inflation. Here's how that looks in UI:

![15-Year Mortgage Payment Components in Indexed Units (UI)](./ui_payment_comps.png)

Three main features should stand out here:
1. More than half of the first payment goes toward paying off interest (which means it doesn't go toward the amount you borrowed), and that proportion decreases over time toward zero.
2. Hence, less than half of the first payment goes toward paying off the principal, and that proportion increases over time until the final payments are almost entirely dedicated to paying off what you borrowed.
3. The total payment stays the same over the course of the loan. For that reason, no portion of the payment (in UI) goes toward compensating inflation.

The story is quite different for UYU:
![15-Year Mortgage Payment Components in Uruguayan Pesos (UYU)](./uyu_payment_comps.png)

A few observations:
1. The same pattern of increasing principal components and decreasing interest components occurs here.  
2. *If there were no inflation,* the total payment would stay the same over the course of the loan.
3. Alas, since your payments are adjusted for inflation, the size of the payment increased over time, and *all of this increase is due to inflation*. Eventually, inflation makes up a big portion of your payments. In March 2012, you're paying around 20,000 pesos per month, and most of that goes toward interest or principal. In March 2021, you're paying double that, around 40,000 pesos, and more than half of that goes toward protecting the bank from inflation.

Finally, let's look at the situation again through the lens of earning income in USD and exchanging USD for UYU to make the payments each month:

![15-Year Mortgage Payment Components in US Dollars (USD)](./usd_payment_comps.png)

We see the same pattern of principal and interest components and the same instability as we saw in [the previous section.](#how-do-ui-relate-to-mortgages) That instability makes calculating your monthly payments in USD fairly uncertain, but it seems like it might work in your favor at times, at least over this timeframe, lessening or even eliminating the impact of inflation in some months. 

I should note before wrapping this up that this example is somewhat falsified, as I'm not privy to the inner workings of BHU. I also ignored fees, since I'm not sure how they're calculated (though I do know they're in UI, not UYU, which means they increase with inflation), and ignoring them doesn't change the story in a meaningful way. Hopefully the example is a useful fiction, and in not-so-broad strokes, I think the story I presented here hews pretty closely to the truth.

## Conclusion

Now, am I saying that this is all bad, that places like BHU are hoodwinking the Uruguayan people and robbing them blind? Not exactly, no. It's not ideal for these financial institutions to pass inflation on to consumers without being super clear about it, but it's probably a greater evil to let these government institutions fall apart and allow economic chaos to ensue.  

However, I got the feeling that people don't exactly know what they're signing up for when they take out a mortgage in Uruguay. While the effects of inflation on the loan might be balanced out by corresponding salary increases, the full depth of the situation and its consequences doesn't seem to be clear from the start. For example, for someone aiming to save a few thousand extra pesos each month to eventually make a lump-sum payment and save themselves a significant amount of money on interest, it might be a rude wake-up call to find that you actually owe more pesos than you did at the start and that the amount you saved up doesn't come close to paying off the loan. My main goal in writing this was to hopefully provide some clarity around this topic, but I think it's even more important for the bank to make the situation clear to potential customers.

Of course, I'm just some dude on the internet writing about a topic outside of my wheelhouse. I wrote about this topic because I was trying to make sense of a problem that didn't make sense to me, but I'm no expert. What did I miss? What am I wrong about? Let me know in the comments what you think.


## Links
- [Historical Consumer Price Index (IPC) Values](https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/estadisticas/series-historicas-ipc-base-octubre-2022100)
- [Historical Indexed Unit (UI) Values](https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/estadisticas/series-historicas-ui)
- [Historical Peso-Dollar (UYU-USD) Conversion Rates](https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/estadisticas/series-historicas-cotizacion%20monedas)