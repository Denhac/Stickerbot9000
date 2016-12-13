Stickerbot9000
==============
StickerBot9000 was a project by members of Denhac to create a donation box that wasn't boring for Mohawkcon at DEFCON 22

About
==============
It consists of a brother QL-700 Label printer, A Raspberry Pi and a salvaged dollar bill collector from some electronic device (We have no idea what one. That's why hacker spaces are awesome). We spent about 2 months putting together 1.0 a

Features
==============
      * Pre-built stickers for printing things.
      * A tiny LCD screen with not nearly enough characters
      * Website to DESIGN YOUR OWN STICKER
      * AP OF AWESOME that redirects even the worst of websites to STICKERBOT (all DNS leads to stickerbot)
      * MONEY TAKING CAPABILITY
      * SMALL IN SIZE
      * Doesn't require alcohol to run.

How it Works
==============
  1. Choose Sticker
  2. Insert Money
  3. Recieve Sticker
  4. ???????????
  5. Profit? (unless, like us you're a non-profit)
  
  In all reality we tried to make it as secure as possible, as this thing was headed to Defcon.
  
  It consists of 3 main systems.
  
    1. The AP.
        Using Hostapd, dnsmasq and a shitty little cheap wifi dongle we set up a custom Access Point. That access point didn't provide any outside web access (security!) and instead dished out DHCP addresses. It also functioned as a DNS server but would always respond to all queries with it's own ip, so that all dns entries went to the custom sticker page.
    
    2. The website.
        This was just Nginx, because we really wanted to have everything as lightweight as possible. It pulled up a javascript editor that saved all pictures to a central images directory. It assigns these files via random number generation for a 5 digit number. 
        
    3. The Backend
        It's a python script that watches that directory for files. When a new file is dropped in, it adds it to the list of possible printing options. A user chooses their own id or a pre-designed id via buttons on the front dashboard, and inserts a dollar. Then the python program pushes the image to the printer and waits until the job is complete. Once the job is complete, if it's a custom sticker it deletes it and preps for the next user.

Results
==============
Stickerbot was of moderate success. Hopefully next year by the time DC23 rolls around we'll have a new and improved stickerbot 2.0 (no idea what number it will actually be.)

Problems
==============
1. Brother is shit at supporting their own printers on anything that is not directly windows/mac or 32bit debian or centos linux. There is source code for the drivers, but this source code doesn't include everything needed to actually run the printer. Solution: Screw them, use the ptouch opensource drivers for the QL-650. With a bit of tweaking these worked perfectly. Serious thanks to Arne John Glenstrup at http://www.diku.dk/~panic/ for working on these. If we were in Denmark we'd buy you a beer.

2. Reading the input from the bill collector itself is a bit of a pain in the ass. Luckally GIPO libraries for raspberry pi are decent and have debounce. Having friends who know basic electronics is awesome.

3. Raspberry Pis are awesome but fragile beasts. Carry spares.

4. So are SD cards.

5. WIFI at a hacker convention is actually a deterrant to using the machine.

6. Your users are never as smart as you thought they would be, and they don't read your signs.

7. We need statistics next time to play sticker eugenics.

Upgrades:
  1. STATISTICS!
  2. Make interface easier to use.
  3. Improve security.
  4. Some kind of self-notifying damage system would be awesome. email? SMS?
  5. The ability to turn on and off the bill acceptor would be nice for interface improvement.
  6. Fix buttons (FIXED)
  7. Make multiple packs of stickers to run
  
Thanks To:
     Denhac - For being there and providing a space for hijinks.
     Krav - Code
     Eric - Code and making the printer work somehow.
     YT   - Case!
     Robb - Moar Case!
     Tek  - Awesome electronics help!
     ChunkyStew - Moar Awesome electronics help.
