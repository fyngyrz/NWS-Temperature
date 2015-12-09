# tmp.py - NWS Temperature Data Fetch

## Tech

Python 2. If you desire Python 3, time to fork.  :\)

## What it Does

Fetches the temperature \(in Cº\) from the NWS aviation ground
conditions forecast by using the `wget` command, the output of which it
pipes back into itself. Then it extracts, then converts, the temperature
value in that forecast to Fahrenheit \(See Below\) or another scale
according to its default `mode` setting  or a supplied command line
option, and prints the result out.

## Limits

The NWS identifies the software that I'm getting the temperature from
\(`getprod.php`\) as "for the whole western region", which I am inclined
to \(wholly incorrectly, as it turns out\) read as "is not for areas
_not_ in the "western region." Which in turn you might be inclined to
view as disappointing if, for instance, you live on the east coast and
really don't care what the weather is in, oh, I don't know, Tempe
Arizona, which I am reasonably sure is somewhere out west, perhaps near
Hawaii or Guam.

Well hey, why should they be consistent? It only scares the cats.
However, as cats have been known on occasion to be scared of things that
aren't there \(they also sometimes attack things that aren't there, but
I digress\), and I have some serious trust issues, I tried New York City
\(`xxxMTRjfk`\) and Miami Florida \(`xxxMTRmia`\), and... both of those worked
fine. As does Los Angeles \(`xxxMTRlax`\) So I don't quite know what to
make of their pronouncement. Obsolete information? Who knows, it's the
USG. "Western region" could mean everything west of Moscow for all I
know. My cats concur, and additionally note that mice exist in all these
regions, so the weather everywhere needs to be known in order that one
doesn't go outside to catch mice and find one's ears and tail exposed to
unacceptably low temperatures.

I find the whole thing inconsistantly consistent, which is consistent
with my general impression of pretty much everything the USG is involved
in.

I should note that Anchorage, AK, \(`xxxMTRanc`\) did *not* work. Despite
being well west of where I am \(IIRC my history, Seward discovered it
somewhere in Russia.\) So there's that, too.

## Configuration

First, change `wgetloc` to the path to the `wget` command, including a
trailing `/` character. For instance, on my system, wget is in
`/usr/local/bin`; so I have set `wgetloc` this way:

```python
wgetloc = '/usr/local/bin/'
```

Next, you probably want to change the `stationid` variable at the top of
the file to the appropriate code for your location. You don't have to, as
this can be set via a command line option \(-s or --station\), but it's
convenient.

The default is `xxxMTRggw` \(some of the most extreme cold temperatures in the nation\), yours will be similar. Thats `xxx`, followed by `MTR`
for the METAR product, and then `ggw` for the NWS weather station ID,
which is actually `kggw`, but I guess the `k` doesn't count, because
government, k?

There is a list of station codes **[on this page](http://www.datasink.com/cgi-bin/stationCodes.cgi)**.

So for instance, I might find a station by searching that page for "Glasgow",
and there it is, Glasgow, "KGGW":

![Station Code Search](http://fyngyrz.com/images/kggw.png)  

I remove the `k`, and construct `xxx` + `MTR` + `ggw` = `xxxMTRggw`
\(Notice the use of lower case instead of upper case, following the example
the NWS provides for doing this.\) It looks like this  on my system:

```python
stationid = "xxxMTRggw"
```

That's the process, but again, this may only work in the "western region."
Which is apparently anything west of Bermuda. Other than Alaska. Which is
apparently east of... something. :)

![West of Bermuda...](http://fyngyrz.com/images/bermuda2.png)  

## Command Line Options

* `-h` or `--help` or `?`
* `-s` or `--station` followed by 3-letter station ID, i.e. `ggw`
* `-m` or `--mode` followed by integer 0...4\*
* `-c` or `--centigrade` \(mode 0\)
* `-f` or `--fahrenheit` \(mode 1\)
* `-k`  or `--kelvin` \(mode 2\)
* `-ra` or `--rankine` \(mode 3\)
* `-re` or `--reaumur` \(mode 4\) \(note use of `e`, not `é`\)

## Other Issues

This Python script has the usual incantation at the top of the file that
tells the operating system how to execute it without having to type
`Python` first:

```
#!/usr/bin/python
```

You might have to change the location so that works.  For instance, to
make it work on both my OS X and my Linux systems, I have to make such a
change. Python is in `/usr/bin/` on one, and `/usr/local/bin` on the
other.

If that's done, then it can be executed in the current directory with
`./tmp.py` instead of `python tmp.py` and it can also be moved to
somewhere in your path \(like `/usr/bin`\) so you can execute it by
typing `tmp.py`

Also worthy of note is that under these circumstances it doesn't care
what it is called, so you can drop the `.py` by renaming it to something
a little easier to type, such as `temp` or whatever, allowing command
line entry of just that, which is yet a little easier.

## Default Operation

With no command line option supplied, the default behavior is to
use the configured default station ID and to
output in degrees Fahrenheit. If you want it to default to degrees
Celsius, Kelvin, Rankine or Réaumur, change `mode` at the top of the Python source code accordingly.
The default mode settings are described in the source code. But be sure
to consider the following:

## Why Fahrenheit is For People. And cats.

Scale | Zero | Twenty Five | Fifty | Seventy Five | 100º  
----- | ---- | ----------- | ----- | ------------ | ---  
 *Celsius* | Cold | Warm | Dead | Dead | Dead  
 *Fahrenheit* | Really Cold | Cold | Meh | Warm | Really Hot  
 *Kelvin* | Dead | Dead | Dead | Dead | Dead  
 *Rankine* | Dead | Dead | Dead | Dead | Dead  
 *Réaumur* | Cold | Hot | Dead | Dead | Dead
Also, look. At -40ºC, it's actually -40ºF.
Isn't that cute? Celsius trying to be reasonable, and all.
Sorry, Celsius. Too low, too late. Back across the pond with you.

So there.
