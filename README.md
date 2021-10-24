# Cryptune
Audio-based cryptography (Python3)

Authored by: Lynden Millington (Fall 2021)

Created under the Clarkson Open Source Institute (COSI)


## **What is Cryptune?**

Cryptune is a program which encodes messages into a series of audio tones. 

While watching a presentation of a fellow peers project which pertained to the encoding and decoding of Morse code,
I became aware of the fact that there are few algorithms and encryption methods which use audio to obscure media, with
Morse being the most prominent. I decided to make my own system of audio encryption, as it seemed like an interesting topic.
Cryptune is the (developing) result.

## **How does Cryptune encode messages?**
Cryptune encodes messages through the use of Grade-1 (uncontracted) Braille. It does so in the following way:

This is the Grade-1 Braille representation of 'H'.
<img src="http://www.byronknoll.com/braille/Braille_h.png" alt="h" width="100" height="140">

Let's split this letter into two columns, with the left column having two dots and the right having only 1.

Next, let's number these dots: 1, 2, and 3, from top to bottom. So, the left column has dots 2 and 3, while the right column has only dot 2.

Now, let's call spaces WITH dots 'ON' and spaces WITHOUT dots 'OFF', or 0 and 1 respectively, and once again represent our columns from top to bottom.

Column 1 is then "110", and Column 2 is subsequently "010". This is now binary representation. The encoded pair for 'H' is 62.

The following is the entire Grade-1 Braille alphabet, which all characters follow.

<img src="https://www.pharmabraille.com/wp-content/uploads/2015/11/braille-alphabet-and-braille-numbers.png" alt="Braille Alphabt">

## **Okay, so we encoded characters into Braille. How does this become audio?**
There's something unique about Braille specifically which makes this process possible. The maximum encoded value for a column using my method is 7 (111, or all three dots.)

Coincidentally, there are also 7 primary notes (not counting microtones) in every octave (A-G).

So, given a base note, an encoded column can be any note within a single octave's range. Here's an example:

> Base = A2. A = 1, B = 2, C = 3, D = 4, E = 5, F = 6, G = 7.

> Encoded H = 62. A2 -> 6 = F, A2 -> 2 = B

> The program will play the notes: F2 B2

## **How to convert note information into sound (Audio Engineering)?**
Fortunately, sound in relation to tone is pretty simple. The frequencies for each note are set values, which can be found in a chart [here.](http://techlib.com/reference/musical_note_frequencies.htm)

However, instead of mapping these all in the program, we can just store a single baseline note, since the entire table can be built around a single value. 
The value you choose could be any value in this table, but to keep it simple, I chose A1 which has a frequency of 55.0 Hz. Some constant rules for generating
tones in this chart are as follows:

> Moving up an octave, but not changing note, such as from A1 -> A2 is just a process of doubling the frequency.

> Moving up any number of notes from a known note, the frequency can be found by taking (known note) x 2^(N/12), where **N** is the number of notes (**INCLUDING MICROTONES, THIS IS IMPORTANT!!**)
> distance between your known note and the one you are trying to find. For example, A1 -> D1 = 55.0Hz x 2^(5/12) = 73.42Hz

There are a number of wave types which can be generated from this calculated frequency, which currently includes **sine, square, and triangle**.
The frequency is the period of these functions, which generates the sound at the proper tones when played back.
