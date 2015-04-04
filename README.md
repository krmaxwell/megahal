To install:

    python setup.py build
    sudo python setup.py install

To run:

    megahal -h

As a lib:

    from megahal import *
    megahal = MegaHAL()
    megahal.train('/path/to/some/file')
    megahal.learn('some phrase')
    print megahal.get_reply('hey, wazzap')
    megahal.sync()  # flush any changes to disc
    megahal.close()  # flush changes and close


