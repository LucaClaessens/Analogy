var request = require('request');
var cheerio = require('cheerio');



for (var i = 1; i < 15; i++) {
    var url = 'http://networkcultures.org/moneylab/page/' + i;

    request(url, (function(pool) {
                    return function(err, resp, body) {
                        $ = cheerio.load(body);
                        $('.box').each(function(day) {
                                var links = $(this).find('a');
                                links.each(function() {
                                        console.log("'"+$(this).attr('href')+"',");
                                });
                        });
                    }
                    })(i));
            }
