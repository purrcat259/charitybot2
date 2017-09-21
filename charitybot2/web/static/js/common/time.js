function convertToDatetime(timestamp){
    if (timestamp >= 2147483647) {
        return 'Heat Death of the Universe';
    }
    return convertToDate(timestamp) + ' ' + convertToTime(timestamp);
}

function convertToDate(timestamp) {
    var d = new Date(timestamp * 1000);
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();

    if (day < 10) {
        day = '0' + day;
    }
    if (month < 10) {
        month = '0' + month;
    }
    return day + '/' + month + '/' + year;
}

function convertToTime(timestamp) {
    var d = new Date(timestamp * 1000);
    var hours = d.getHours();
    var minutes = d.getMinutes();
    var seconds = d.getSeconds();
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }
    if (seconds < 10) {
        seconds = '0' + seconds;
    }
    return hours + ':' + minutes + ':' + seconds;
}

function roundUp(number) {
    return Math.round(number * 100) / 100;
}

function returnTimespanString(timespanInSeconds) {
    var timespanInMinutes = timespanInSeconds / 60;
    if (timespanInMinutes < 1) {
        return roundUp(timespanInSeconds) + ' seconds';
    } else if (timespanInMinutes == 1) {
        return '1 second';
    }
    var timespanInHours = timespanInMinutes / 60;
    if (timespanInHours < 1) {
        return Math.floor(timespanInMinutes) + ' minutes';
    } else if (Math.floor(timespanInMinutes) == 1) {
        return '1 minute';
    }
    if (timespanInHours == 1) {
        return '1 hour';
    }
    return roundUp(timespanInHours) + ' hours';
}