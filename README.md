# tmp.py - NWS Temperature Data Fetch

## What it Does

Fetches the temperature (in Cº) from the NWS aviation ground conditions
forecast. Then it converts that value to Fahrenheit \(See Below\) or another
scale according to its `mode` setting, and prints the result out.

## Limits

The NWS identifies the software that I'm getting the temperature from
as "for the whole western region", from which I take it that it is not
for areas _not_ in the "western region." Well hey, why be consistent?
It only scares the cats.

So for the moment, be aware of that. I'll try and figure out if the...
eastern\(?\) region\(s\) use\(s\) the same software at a different URL, and if
I find that to be the case, I'll update the project to deal with it
somehow.

## Configuration

Change the **stationid** variable at the top of the file to the
appropriate code for your location.

Mine is "xxxMTRggw", yours will be similar. Thats xxx, followed by MTR
for the METAR product, and then "ggw" for my NWS weather station ID,
which is actually "kggw", but I guess the "k" doesn't count.

I'm also working on trying to come up with an easy process to let you
dig up what your local code will be. The NWS doesn't make finding it out
obvious, like, "enter your zip code here." :\)

The default is to output in degrees Fahrenheit. If you want degrees
Celsius, Kelvin, Rankine or Réaumur, set `mode` at the top of the python source code.
The modes are described in the source code. But be sure to read the following:

## Why Fahrenheit is For People

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
