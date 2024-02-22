companies_by_ticker_response = {
    "company_ticker": "AAPL",
    "company_name": "Apple Inc.",
    "company_top_themes": '["audio-products", "cloud-computing", "manufacturing"]',
    "company_description": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.",
}

companies_by_ticker_bad_request_response = {
    "detail": "Invalid ticker. Up to 6 capital letters only."
}

companies_by_ticker_not_found_response = {
    "detail": "No company found with given ticker: AAPL"
}

company_tickers_by_theme_name_response = {
    "theme_name": "manufacturing",
    "number_of_matches": 2,
    "data": ["AAPL", "TSLA"],
}

company_tickers_by_theme_name_bad_request_response = {
    "detail": "invalid theme:a\nAccepted themes:['electric-vehicles', 'manufacturing', 'solar-energy', 'mobile-phones', 'telecommunications', 'audio-products', 'cloud-computing', 'retail', 'e-commerce', 'consumer-products']"
}

company_tickers_by_theme_name_not_found = {
    "detail": "No companies found with theme name: manufacturing"
}

internal_server_error_response = {"detail": "Internal Server Error."}
