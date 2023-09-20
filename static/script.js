$(document).ready(function () {
    // Load ticker symbols and populate the ticker list
    $.getJSON('/get_tickers', function (data) {
        console.log("Received Data:", data);
        if (!data || !data.tickers) {
            console.error("Invalid response from the server");
            return;
        }

        var tickerList = $('#ticker-list');
        var tickerItems = data.tickers.map(function (ticker) {
            var tickerItem = $('<div>', {
                class: 'ticker-item',
                text: ticker.name
            }).on('click', function () {
                loadCompanyDetails(ticker.symbol);
                $('.ticker-item').removeClass('selected');
                $(this).addClass('selected');
            });
            return tickerItem;
        });
        tickerList.empty().append(tickerItems);
    });
});


function loadCompanyDetails(ticker) {
        // Show loading overlay
        var loadingOverlay = document.getElementById('loading-overlay');
        loadingOverlay.style.display = 'block';

        // Apply blur to the company data section
        var companyDataSection = document.getElementById('company-data');
        companyDataSection.style.filter = 'blur(5px)';

    $.getJSON('/get_company_data/' + ticker, function (data) {

        var companyData = data.company_data;
        var incomeStatement = data.income_statement;
        var balanceSheet = data.balance_sheet; // Add this line
        var cashFlowStatement = data.cash_flow_statement; // Add this line

        var companyDetailsTable = $('#company-data-table');
        companyDetailsTable.empty();

        var keysToShow = [
            'longName', 'symbol', 'longBusinessSummary',
            'sharesOutstanding', 'marketCap'
        ];

        var labels = {
            'longName': 'Company Name',
            'symbol': 'Company Ticker',
            'longBusinessSummary': 'Company Description',
            'sharesOutstanding': 'Shares Outstanding',
            'marketCap': 'Market Cap (JPY)'
        };

        for (var i = 0; i < keysToShow.length; i++) {
            var key = keysToShow[i];
            var value = companyData[key];

            if (typeof value === 'number') {
                value = value.toLocaleString('en-US');
            }

            var row = $('<tr>').appendTo(companyDetailsTable);
            $('<th>', { text: labels[key] }).appendTo(row);
            $('<td>', { text: value }).appendTo(row);
        }

        //Update table display in html
        // Update the table display in the HTML under #statistics
//        var financialTable = $('<table>').html(data.financial_table);  // Convert the HTML string to a table element
//        $('#statistics').empty().append($('<h3>').text('Financial Metrics'));
//        $('#statistics').append(financialTable);


        // Income Statement
        var incomeStatementTable = $('#income-statement-table');
        incomeStatementTable.empty();
        var incomeStatementData = incomeStatement.data.reverse();
        var incomeStatementLabels = incomeStatement.index.reverse();
        var columnsIS = incomeStatement.columns;

        // Create header rows
        var headerRowIncomeStatement = $('<tr>').appendTo(incomeStatementTable);
        $('<th>', { text: 'Item' }).appendTo(headerRowIncomeStatement); // Label cell
        columnsIS.forEach(function (column, columnIndex) {
            $('<th>', { text: new Date(column).toDateString() }).appendTo(headerRowIncomeStatement);
        });

        //create dataa rows
        incomeStatementLabels.forEach(function (label, labelIndex){
            var dataRow = $('<tr>').appendTo(incomeStatementTable);
            $('<td>', {text:label}).appendTo(dataRow);
            var rowData = incomeStatementData[labelIndex];
            rowData.forEach(function(value){
                var formattedValue = value != null ? value.toLocaleString('en-US',{maximumFractionDigits:0}): 'N/A';
                $('<td>',{text:formattedValue}).appendTo(dataRow);
            });
        });

        //balance sheet
        var balanceSheetTable = $('#balance-sheet-table');
        balanceSheetTable.empty();
        var balanceSheetData = balanceSheet.data.reverse();
        var balanceSheetLabels = balanceSheet.index.reverse();
        var columnsBS = balanceSheet.columns;

        // Create header rows
        var headerRowBalanceSheet = $('<tr>').appendTo(balanceSheetTable);
        $('<th>', { text: 'Item' }).appendTo(headerRowBalanceSheet); // Label cell
        columnsBS.forEach(function (column, columnIndex) {
            $('<th>', { text: new Date(column).toDateString() }).appendTo(headerRowBalanceSheet);
        });

        //create dataa rows
        balanceSheetLabels.forEach(function (label, labelIndex){
            var dataRow = $('<tr>').appendTo(balanceSheetTable);
            $('<td>', {text:label}).appendTo(dataRow);
            var rowData = balanceSheetData[labelIndex];
            rowData.forEach(function(value){
                var formattedValue = value != null ? value.toLocaleString('en-US',{maximumFractionDigits:0}): 'N/A';
                $('<td>',{text:formattedValue}).appendTo(dataRow);
            });
        });

        //cash flow statement
        var cashFlowStatementTable = $('#cash-flow-statement-table');
        cashFlowStatementTable.empty();
        var cashFlowStatementData = cashFlowStatement.data.reverse();
        var cashFlowStatementLabels = cashFlowStatement.index.reverse();
        var columnCFS = cashFlowStatement.columns;

        // Create header rows
        var headerRowCashFlowStatement = $('<tr>').appendTo(cashFlowStatementTable);
        $('<th>', { text: 'Item' }).appendTo(headerRowCashFlowStatement); // Label cell
        columnCFS.forEach(function (column, columnIndex) {
            $('<th>', { text: new Date(column).toDateString() }).appendTo(headerRowCashFlowStatement);
        });

        //create dataa rows
        cashFlowStatementLabels.forEach(function (label, labelIndex){
            var dataRow = $('<tr>').appendTo(cashFlowStatementTable);
            $('<td>', {text:label}).appendTo(dataRow);
            var rowData = cashFlowStatementData[labelIndex];
            rowData.forEach(function(value){
                var formattedValue = value != null ? value.toLocaleString('en-US',{maximumFractionDigits:0}): 'N/A';
                $('<td>',{text:formattedValue}).appendTo(dataRow);
            });
        });
        loadingOverlay.style.display = 'none';
        companyDataSection.style.filter = 'none';
    });
}


