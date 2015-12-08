# tmp.py - NWS Temperature Data Fetch

## What it Does

Fetches the temperature \(in Cº\) from the NWS aviation ground conditions
forecast by using the `wget` command, the output of which it pipes
back into itself. Then it extracts, then converts, the temperature value
in that forecast to Fahrenheit \(See Below\) or another scale according
to its `mode` setting, and prints the result out.

## Limits

The NWS identifies the software that I'm getting the temperature from
as "for the whole western region", which I would read as "is not
for areas _not_ in the "western region." Well hey, why be consistent?
It only scares the cats.

However, as cats have been known on occasion to be scared of nothing, I
tried New York City \(xxxMTRjfk\) and Miami Florida \(xxxMTRmia\), and
both of those worked fine. As does Los Angeles \(xxxMTRlax\) So I don't
quite know what to make of their pronouncement. Obsolete information?
Who knows, it's the USG. "Western region" could mean everything west of
Moscow for all I know. My cats concur, and additionally note that mice
exist in all these regions, so the weather everywhere needs to be known
in order that one doesn't go outside to catch mice and find one's ears
and tail exposed to unacceptably low temperatures.

## Configuration

First, change `wgetloc` to the path to the `wget` command, including a
trailing `/` character. For instance, on my system, wget is in
`/usr/local/bin`; so I have set `wgetloc` this way:

```python
wgetloc = '/usr/local/bin/'
```

Next, change the `stationid` variable at the top of the file to the
appropriate code for your location.

Mine is "xxxMTRggw", yours will be similar. Thats xxx, followed by MTR
for the METAR product, and then "ggw" for my NWS weather station ID,
which is actually "kggw", but I guess the "k" doesn't count, because
government, k?

There is a list of station codes **[on this page](http://www.datasink.com/cgi-bin/stationCodes.cgi)**.

So for instance, I find my station by searching that page for "Glasgow",
and there it is, Glasgow MT, "KGGW":

![Station Code Search](http://fyngyrz.com/images/kggw.png)  

I remove the k, and construct xxx + MTR + ggw = xxxMTRggw  \(Notice
the use of lower case instead of upper case, following the example
the NWS provides for doing this.\) It looks like this  on my system:

```python
stationid = "xxxMTRggw"
```

That's the process, but again, this may only work in the "western region."
Which is apparently anything west of Bermuda. :)

![West of Bermuda...](http://fyngyrz.com/images/bermuda2.png)  

The default is to output in degrees Fahrenheit. If you want degrees
Celsius, Kelvin, Rankine or Réaumur, set `mode` at the top of the python source code.
The modes are described in the source code. But be sure to consider the
following:

## Why Fahrenheit is For People. And cats.

Scale | Zero | Twenty Five | Fifty | Seventy Five | 100º  
----- | ---- | ----------- | ----- | ------------ | ---  
 *Celsius* | Cold | Warm | Dead | Dead | Dead  
 *Fahrenheit* | Really Cold | Cold | Meh | Warm | Really Hot  
 *Kelvin* | Dead | Dead | Dead | Dead | Dead  
 *Rankine* | Dead | Dead | Dead | Dead | Dead  
 *Réaumur* | Cold | Hot | Dead | Dead | Dead
Also, look. At -40ºc, it's actually -40ºF.
Isn't that cute? Celsius trying to be reasonable, and all.
Sorry, Celsius. Too low, too late. Back across the pond with you.

So there.
