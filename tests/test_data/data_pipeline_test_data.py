test_company_html = """<HTML>
<HEAD>
<TITLE>Company Description: Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1>Apple Inc.</H1>
<H2>Ticker: AAPL</H2>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_description = """Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card."""

test_invalid_html_format = """"<HTML>
<HEAD>
</HEAD>
<BODY>
<H1>Apple Inc.</H1>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_html_no_ticker = """<HTML>
<HEAD>
<TITLE>Company Description: Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1>Apple Inc.</H1>
<H2>Ticker AAPL</H2>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_blank_company_name = """<HTML>
<HEAD>
<TITLE>Company Description: Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1></H1>
<H2>Ticker AAPL</H2>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_missing_title_prefix = """<HTML>
<HEAD>
<TITLE>Company Description Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1>Apple Inc.</H1>
<H2>Ticker: AAPL</H2>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_mismatch_name = """<HTML>
<HEAD>
<TITLE>Company Description: Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1>Apple Incorporated</H1>
<H2>Ticker: AAPL</H2>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_missing_ticker_prefix = """<HTML>
<HEAD>
<TITLE>Company Description: Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1>Apple Inc.</H1>
<H2>AAPL</H2>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_blank_ticker_prefix = """<HTML>
<HEAD>
<TITLE>Company Description: Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1>Apple Inc.</H1>
<H2>Ticker:</H2>
<P>
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops,
    and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the 
    U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, 
    the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media 
    player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, 
    macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and 
    iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online 
    services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud.
    Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.
</P>
</BODY>
</HTML>"""

test_company_blank_description = """<HTML>
<HEAD>
<TITLE>Company Description: Apple Inc.</TITLE>
</HEAD>
<BODY>
<H1>Apple Inc.</H1>
<H2>Ticker: AAPL</H2>
<P></P>
</BODY>
</HTML>"""

test_parse_themes_output = {
    "theme1": {
        "theme_name": "theme1",
        "theme_description": "description1",
        "theme_description_model_encoding": "test encode value",
    },
    "theme2": {
        "theme_name": "theme2",
        "theme_description": "description2",
        "theme_description_model_encoding": "test encode value",
    },
}

sample_processed_themes = {
    "theme1": {
        "theme_name": "theme1",
        "theme_description": "description1",
        "theme_description_model_encoding": "encoded description1",
    }
}

sample_processed_companies = {
    "company1": {
        "company_name": "company1",
        "company_description": "description1",
        "company_description_model_encoding": "encoded description1",
    }
}

sample_determine_themes_output = {
    "company1": {
        "company_ticker": "company1",
        "company_name": "company1",
        "company_top_themes": ["theme1"],
        "company_description": "description1",
    }
}
