var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;
var donationsUrl = eventUrl + '/donations/';

var currencySymbol = 'N/A';
var updateDelay = 2000; // ms


// Get the currency symbol then setup the updating cycle
getCurrencySymbol().then((symbol) => {
    currencySymbol = symbol;
    updateTicker(numberOfDonations);
    setInterval(
        () => {
            updateTicker(numberOfDonations);
        },
        updateDelay
    );
}).catch((error) => {
    console.error(error);
});

function updateTicker(limit) {
    console.log('Updating ticker');
    fetchJSONFile(
        donationsUrl + '?limit=' + limit,
        (response) => {
            drawTableRows(response);
        },
        () => {
            console.error('Unable to connect to retrieve donations');
        }
    );
}

function drawTableRows(data) {
    var table = document.getElementById('ticker-table');
    var tableHeader = '<tr><th>Latest Donations</th></tr>';
    table.innerHTML = '';
    table.innerHTML = tableHeader;
    var tableRows = '';
    for (var i = 0; i < data.donations.length; i++) {
        var donation = JSON.parse(data.donations[i]);
        var donationRow = '<tr><td>' + currencySymbol + donation['amount'] + ', ' + returnTimespanString(donation['timestamp']) + ' ago</td></tr>';
        tableRows += donationRow;
    }
    table.innerHTML += tableRows;
}