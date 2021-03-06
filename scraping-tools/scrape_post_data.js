var request = require('request');
var cheerio = require('cheerio');

pages = [
    'http://networkcultures.org/moneylab/2015/12/14/degenerated-political-art-by-nuria-guell-levi-orta/',
    'http://networkcultures.org/moneylab/2015/12/11/raluca-croitoru-immaterial-institute-of-research-and-experimentation/',
    'http://networkcultures.org/moneylab/2015/12/11/primavera-de-filippi-blockchain-technology-as-distributed-governance-tool/',
    'http://networkcultures.org/moneylab/2015/12/11/stephanie-rothenberg-reversal-of-fortune-visualizing-marketized-philanthropy/',
    'http://networkcultures.org/moneylab/2015/12/11/equitybot-by-scott-kildall/',
    'http://networkcultures.org/moneylab/2015/12/11/algorithmic-autonomy-freedom-and-the-blockchain/',
    'http://networkcultures.org/moneylab/2015/12/11/workshop-negotiating-trust-on-crowdfunding-platforms-by-robert-van-boeschoten/',
    'http://networkcultures.org/moneylab/2015/12/11/commoneasy-a-new-p-2-p-insurance-model-is-born/',
    'http://networkcultures.org/moneylab/2015/12/11/bringing-the-dark-side-of-money-to-light-paul-radu/',
    'http://networkcultures.org/moneylab/2015/12/11/silvio-lorusso-on-meta-failure-and-the-dark-side-of-crowdfunding/',
    'http://networkcultures.org/moneylab/2015/12/16/panel-and-audience-discussion-artistic-interventions-in-finance/',
    'http://networkcultures.org/moneylab/2015/12/15/femke-herregraven-the-privilege-of-disappearing/',
    'http://networkcultures.org/moneylab/2015/12/15/tactics-for-economies-dissent-panel-introduction-by-brett-scott/',
    'http://networkcultures.org/moneylab/2015/12/15/venture-communism-baruch-gottlieb-and-dmitry-kleiner/',
    'http://networkcultures.org/moneylab/2015/12/15/rachel-odwyer-storing-value/',
    'http://networkcultures.org/moneylab/2015/12/15/eduard-de-jong-a-short-history-of-the-blockchain/',
    'http://networkcultures.org/moneylab/2015/12/15/panel-discussion-bringing-the-dark-side-of-money-to-light/',
    'http://networkcultures.org/moneylab/2015/12/15/bruce-pon-ascribe-an-ownership-layer-for-the-internet/',
    'http://networkcultures.org/moneylab/2015/12/14/2378/',
    'http://networkcultures.org/moneylab/2015/12/14/dulltech-neoliberal-hardware-lulz/',
    'http://networkcultures.org/moneylab/2016/09/09/steven-hill-on-the-necessity-of-regulating-services-like-airbnb-and-uber/',
    'http://networkcultures.org/moneylab/2016/09/08/on-demand-economy-more-regulations-and-non-profit-apps-needed-to-build-a-fairer-future/',
    'http://networkcultures.org/moneylab/2016/07/12/%c2%adblockchain-bureaucracy/',
    'http://networkcultures.org/moneylab/2016/07/12/first-confirmed-speakers-for-moneylab-3-failing-better/',
    'http://networkcultures.org/moneylab/2016/07/07/tickets-moneylab-3-failing-better-now-available/',
    'http://networkcultures.org/moneylab/2016/06/23/matthew-slater-on-scaling-trust-with-credit-commons-part-2/',
    'http://networkcultures.org/moneylab/2016/06/21/matthew-slater-on-scaling-trust-with-credit-commons/',
    'http://networkcultures.org/moneylab/2016/06/10/fully-automated-luxury-communism/',
    'http://networkcultures.org/moneylab/2016/06/06/highlights-from-ouishare-2016/',
    'http://networkcultures.org/moneylab/2016/05/17/we-are-hiring-an-intern-for-moneylab3/',
    'http://networkcultures.org/moneylab/2015/10/23/brett-scott-talks-to-paul-buitink/',
    'http://networkcultures.org/moneylab/2015/10/07/thoughts-on-a-cashless-society/',
    'http://networkcultures.org/moneylab/2015/10/02/report-from-reinvent-money/',
    'http://networkcultures.org/moneylab/2015/09/30/crowdfest-report/',
    'http://networkcultures.org/moneylab/2015/09/24/creativity-on-the-blockchain/',
    'http://networkcultures.org/moneylab/2015/09/21/moneylab2-economies-of-dissent-flyer/',
    'http://networkcultures.org/moneylab/2015/09/03/save-the-date-moneylab2-economies-of-dissent/',
    'http://networkcultures.org/moneylab/2015/09/03/the-bitcoin-experience-part-two/',
    'http://networkcultures.org/moneylab/2015/04/21/the-moneylab-reader-is-now-available/',
    'http://networkcultures.org/moneylab/2014/12/16/one-chain-to-rule-them-all/',
    'http://networkcultures.org/moneylab/2016/04/29/temporary-marriages-in-a-blockchain-city/',
    'http://networkcultures.org/moneylab/2016/04/21/moneylab3-failing-better/',
    'http://networkcultures.org/moneylab/2016/04/13/re-designing-democracy/',
    'http://networkcultures.org/moneylab/2016/04/04/financial-reporting-on-the-panama-papers-and-speculative-outcomes/',
    'http://networkcultures.org/moneylab/2016/03/21/promise-of-the-blockchain/',
    'http://networkcultures.org/moneylab/2016/02/01/symposium-report-moneylab2-economies-of-dissent-is-now-ready/',
    'http://networkcultures.org/moneylab/2016/01/26/moneylab-internship/',
    'http://networkcultures.org/moneylab/2016/01/06/capturing-the-essence-of-moneylab/',
    'http://networkcultures.org/moneylab/2015/12/17/eric-duran-economic-disobedience/',
    'http://networkcultures.org/moneylab/2015/12/16/panel-and-audience-discussion-tactics-for-economic-dissent/',
    'http://networkcultures.org/moneylab/2014/04/04/visualizing-crowdfunding-and-beyond/',
    'http://networkcultures.org/moneylab/2014/04/04/call-for-contributions-the-inc-moneylab-reader/',
    'http://networkcultures.org/moneylab/2014/04/02/brett-scott-applying-the-hacker-ethic-to-the-financial-system/',
    'http://networkcultures.org/moneylab/2014/04/01/jerome-roos-writes-reflections-on-moneylab-in-each-other-we-trust-coining-alternatives-to-capitalism/',
    'http://networkcultures.org/moneylab/2014/04/01/franco-berardi-money-language-insolvency/',
    'http://networkcultures.org/moneylab/2014/03/31/ron-peperkamp-and-the-art-reserve-bank/',
    'http://networkcultures.org/moneylab/2014/03/29/mobile-money/',
    'http://networkcultures.org/moneylab/2014/03/29/tiziana-terranova-virtual-money-and-the-currency-of-the-commons/',
    'http://networkcultures.org/moneylab/2014/03/28/non-money/',
    'http://networkcultures.org/moneylab/2014/03/28/mobile-money-and-the-social-and-technological-infrastructures-of-transaction/',
    'http://networkcultures.org/moneylab/2015/12/11/workshop-avenging-money-by-max-haiven/',
    'http://networkcultures.org/moneylab/2015/12/10/free-money-movement-the-commons-a-workshop-by-jim-costanzo/',
    'http://networkcultures.org/moneylab/2015/12/02/dmytri-kleiner-baruch-gottlieb-join-moneylab2-to-talk-about-venture-communism/',
    'http://networkcultures.org/moneylab/2015/11/30/10-bitcoin-myths/',
    'http://networkcultures.org/moneylab/2015/11/30/money-2020/',
    'http://networkcultures.org/moneylab/2015/11/26/unpacking-platform-cooperativism/',
    'http://networkcultures.org/moneylab/2015/11/23/moneylab-program-booklet-is-finalized/',
    'http://networkcultures.org/moneylab/2015/11/16/whats-wrong-with-get-played-get-paid-campaign/',
    'http://networkcultures.org/moneylab/2015/10/28/geographies-of-imagination/',
    'http://networkcultures.org/moneylab/2015/10/23/the-rise-of-social-exchange-systems/',
    'http://networkcultures.org/moneylab/2014/10/16/moneylab-at-the-dutch-design-week/',
    'http://networkcultures.org/moneylab/2014/09/19/digital-cash-conference-at-ucla-27-28-september-2014/',
    'http://networkcultures.org/moneylab/2014/06/10/money-and-art-an-interview-with-max-haiven-in-crit/',
    'http://networkcultures.org/moneylab/2014/06/06/crowdfunding-theory-under-construction-report-from-amsterdams-first-academic-research-seminar/',
    'http://networkcultures.org/moneylab/2014/05/27/reader-of-tulipomania-dotcom-2000-again-available/',
    'http://networkcultures.org/moneylab/2014/05/27/bitcoin-2014-report/',
    'http://networkcultures.org/moneylab/2014/05/19/its-all-in-the-code-report-from-the-dutch-national-bitcoin-congres/',
    'http://networkcultures.org/moneylab/2014/05/07/european-commission-call-for-experts-on-crowdfunding/',
    'http://networkcultures.org/moneylab/2014/04/25/in-art-we-trust-the-art-reserve-bank/',
    'http://networkcultures.org/moneylab/2014/04/14/crowdfunding-regulation-developments-and-possible-implications-part-1-europe/',
    'http://networkcultures.org/moneylab/2014/01/30/introducing-moneylab-speakers-dette-glashouwer/',
    'http://networkcultures.org/moneylab/2014/01/27/moneylab-news-conference-program-tickets-online/',
    'http://networkcultures.org/moneylab/2014/03/13/moneylab-conference-bazaar-workshops-film-program/',
    'http://networkcultures.org/moneylab/2014/03/13/the-arts-economic-nexus/',
    'http://networkcultures.org/moneylab/2014/03/12/stephan-musoke/',
    'http://networkcultures.org/moneylab/2014/03/06/investment-crowdfunding-for-film/',
    'http://networkcultures.org/moneylab/2014/03/06/moneylab-program-booklet/',
    'http://networkcultures.org/moneylab/2014/01/23/introducing-moneylab-speakers-brett-scott-on-open-source-finance/',
    'http://networkcultures.org/moneylab/2014/01/23/alternative-currencies-become-more-popular-in-the-netherlands/',
    'http://networkcultures.org/moneylab/2014/01/20/crowdfunding-determinants-of-success-and-failure/',
    'http://networkcultures.org/moneylab/2014/01/06/upcoming-event-new-industries-conference-by-hmvk-dortmund/',
    'http://networkcultures.org/moneylab/2014/01/06/m0n3y-as-an-3rror-online-exhibition/',
    'http://networkcultures.org/moneylab/2014/03/28/finance-is-not-about-money/',
    'http://networkcultures.org/moneylab/2014/03/28/mobile-money-and-social-or-anti-social-security/',
    'http://networkcultures.org/moneylab/2014/03/28/1240/',
    'http://networkcultures.org/moneylab/2014/03/27/peer-do-a-laboratory-for-co-funded-action/',
    'http://networkcultures.org/moneylab/2014/03/27/peer-to-peer-or-mine-to-mine-a-critique-of-crowdfunding/',
    'http://networkcultures.org/moneylab/2014/03/27/overcoming-the-legitimacy-crisis-of-money-with-bitcoin/',
    'http://networkcultures.org/moneylab/2014/03/27/bitcoin-leveraging-cryptography-against-the-control-society/',
    'http://networkcultures.org/moneylab/2014/03/27/the-dark-arts-of-reimagining-money/',
    'http://networkcultures.org/moneylab/2014/03/27/always-sunny-in-the-rich-mans-world/',
    'http://networkcultures.org/moneylab/2014/03/27/eli-gothill-from-the-muslim-trade-routes-to-twitters-punkmoney/',
    'http://networkcultures.org/moneylab/2014/01/30/moneylab-at-transmediale-festival-berlin/',
    'http://networkcultures.org/moneylab/2014/02/03/bitcoin-explained-daniel-forrester-mark-solomon-a-review/',
    'http://networkcultures.org/moneylab/2014/02/06/the-social-coin-that-tracks-and-measures-good-actions/',
    'http://networkcultures.org/moneylab/2014/02/18/sign-up-for-a-crowdfunding-workshop/',
    'http://networkcultures.org/moneylab/2014/02/19/848/',
    'http://networkcultures.org/moneylab/2014/02/21/have-you-used-crowdfunding-we-need-your-input/',
    'http://networkcultures.org/moneylab/2014/02/27/873/',
    'http://networkcultures.org/moneylab/2014/03/03/critical-finance-in-amsterdam-august-13-15-2014/',
    'http://networkcultures.org/moneylab/2014/03/04/moneylab-party/',
    'http://networkcultures.org/moneylab/2014/03/05/international-womens-day-on-indiegogo/',
    'http://networkcultures.org/moneylab/2014/03/27/cryptocurrencies-designing-alternatives/',
    'http://networkcultures.org/moneylab/2014/03/27/brian-holmes-consequences-of-quantitative-easing/',
    'http://networkcultures.org/moneylab/2014/03/26/hashtag-moneylab/',
    'http://networkcultures.org/moneylab/2014/03/26/they-say-money-doesnt-grow-on-trees-dadara-proves-us-otherwise/',
    'http://networkcultures.org/moneylab/2014/03/25/1050/',
    'http://networkcultures.org/moneylab/2014/03/24/peter-surda-some-misconceptions-about-bitcoin-and-why-it-is-best-left-ungoverned/',
    'http://networkcultures.org/moneylab/2014/03/23/fresh-projects-in-the-alternatives-bazaar/',
    'http://networkcultures.org/moneylab/2014/03/23/edward-de-jong-towards-an-open-e-currency-system/',
    'http://networkcultures.org/moneylab/2014/03/23/bill-maurer/',
    'http://networkcultures.org/moneylab/2014/03/18/ending-the-moneylab-event-in-hacking-style/',
    'http://networkcultures.org/moneylab/2013/12/19/media-narratives-on-bitcoin-common-arguments-against-the-crypto-currency/',
    'http://networkcultures.org/moneylab/2013/12/13/media-narratives-on-bitcoin-7-common-arguments-in-favor-of-the-crypto-currency/',
    'http://networkcultures.org/moneylab/2013/12/02/hidden-transaction-systems-of-free-culture-and-free-culture-entrepreneurs/',
    'http://networkcultures.org/moneylab/2013/11/29/moneylab-blog-is-live/',
    'http://networkcultures.org/moneylab/2013/11/29/more-than-currency-the-importance-of-bitcoin-as-a-technology-and-financial-model/',
    'http://networkcultures.org/moneylab/2013/11/28/documentary-making-in-uk-between-broadcasters-funding-and-online-revenue-models/',
    'http://networkcultures.org/moneylab/2013/11/26/new-york-times-three-years-of-kickstarter-a-start-in-researching-crowdfunding-dynamics/',
    'http://networkcultures.org/moneylab/2013/10/30/out-now-disrupting-business-art-and-activism-in-times-of-financial-crisis/',
    'http://networkcultures.org/moneylab/2013/10/11/the-institute-of-network-cultures-presents-moneylab-coining-alternatives/',
    'http://networkcultures.org/moneylab/2014/01/30/crowdfunding-redistributing-wealth-or-monetizing-social-relations/'
];



for (page in pages) {
    var url = pages[page];

    request(url, (function(www) {
        return function(err, resp, body) {
            $ = cheerio.load(body);
            $('.entry-content').each(function(q) {
                var lines = $(this).children('p').text().split('.');
                for (var i = lines.length - 1; i >= 0; i--) {
                    if (lines[i].length > 10 && lines[i] != "Design and development by Roberto Picerno & Silvio Lorusso.") {
                        console.log(lines[i] + '.');
                    }
                }


            });
        }
    })(page));
}
