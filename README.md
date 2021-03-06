# tmp.py - NWS Temperature Data Fetch

## What it Does

Fetches the temperature \(in Cº\) from the NWS aviation ground
conditions forecast by using the `wget` command, the output of which it
pipes back into itself. Then it extracts, then converts, the temperature
value in that forecast to Fahrenheit \(See Below\) or another scale
according to its default `mode` setting  or a supplied command line
option, and prints the result out.

## Requirements

* Known Working Under:
  * rPi, Raspbian, 7.6
  * OS X 10.6.8 \(Snow Leopard\)
  * Ubuntu 12.04.5 LTS \(Precise Pangolin\)
* Python 2.6 or 2.7 \(If you desire Python 3, time to fork.\)
* Standard Python imports: `sys`, `subprocess`
* Network connection w/DNS
* `wget` command

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
\(`jfk`\) and Miami Florida \(`mia`\), and... both of those worked
fine. As does Los Angeles \(`lax`\) So I don't quite know what to
make of their pronouncement. Obsolete information? Who knows, it's the
USG. "Western region" could mean everything west of Moscow for all I
know. My cats concur, and additionally note that mice exist in all these
regions, so the weather everywhere needs to be known in order that one
doesn't go outside to catch mice and find one's ears and tail exposed to
unacceptably low temperatures.

I find the whole thing inconsistantly consistent, which is consistent
with my general impression of pretty much everything the USG is involved
in.

I should note that Anchorage, AK, \(either of `anc` or `aed`\) did *not*
work. Despite being well west of where I am \(IIRC my history, Seward
discovered it somewhere in Russia.\) So there's that, too. On second
thought, perhaps they simply want us to take "western region" to mean
"south of Canada."

## Configuration

You probably want to change the `stationid` variable at the top of
the file to the appropriate code for your location. You don't have to, as
this can be set via a command line option \(-s or --station\), but it's
convenient so you can just run the command with no parameters and get
the temperature you're most often interested in.

The default is `ggw` \(some of the most extreme cold temperatures in the
nation, so kind of fun\), yours will be a different three-letter code.

There is a list of station codes **[on this page](http://www.datasink.com/cgi-bin/stationCodes.cgi)**.

So for instance, I might find a station by searching that page for "Glasgow",
and there it is, Glasgow, "KGGW":

![Station Code Search](http://fyngyrz.com/images/kggw.png)  

Remove the first letter, and use the remaining three.
The station code you put in is not case-sensitive.
The default looks like this:

```python
stationid = "ggw"
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

This Python program has the usual incantation at the top of the file
that tells \*nix-flavored operating systems how to execute it without
having to type `python` first:

```python
#!/usr/bin/python
```

You might have to change that so your system will know how to do this. 
For instance, to make it work on both my OS X and my Linux systems, I
have to make such a change. Python is in `/usr/bin` on one, but
`/usr/local/bin` on the other.

If that line is correctly set up for your system, then the program can
be executed in the current directory with `./tmp.py` instead of `python
tmp.py` and it can also be moved to somewhere in your path \(like
`/usr/bin`\) so you can execute it by typing `tmp.py`

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
