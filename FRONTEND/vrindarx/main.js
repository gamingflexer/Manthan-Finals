
const searchButtonTag = document.querySelector("main div.stage1Keyword form button[type=submit]");
const mainTag = document.querySelector("main");
const stageTitleTag = document.querySelector("header p");
const stage1ScrapingButtonTag = document.querySelector("main div.stage1Scraping button");
const tweetsFoundCounterTag = document.querySelector("main div.stage1Scraping p.counting b");
const stage2RecordsTableBodyTag = document.querySelector("main div.stage2Records table tbody");
const stage2RecordsButtonTag = document.querySelector("main div.stage2Records button");
const stage3NetworkButtonTag = document.querySelector("main div.stage3Network button");
const stage4SusTableBodyTag = document.querySelector("main div.stage4Sus table tbody");
const headerStageCounterTags = document.querySelectorAll("header div");

const accountsFoundJSONpath = "./2.json";
const networkChartJSONpath = "./network.json";
const susAccountsFoundJSONpath = "./3.json";

function addEventListeners() {
    searchButtonTag.onclick = function(evt) {
        evt.preventDefault();
        enableStage1Scraping();
    };
    stage1ScrapingButtonTag.onclick = function(evt) {
        evt.preventDefault();
        enableStage2Records();
    };
    stage2RecordsButtonTag.onclick = function(evt) {
        evt.preventDefault();
        enableStage3Network();
    };
    stage3NetworkButtonTag.onclick = function(evt) {
        evt.preventDefault();
        enableStage4Sus();
    };
};

addEventListeners();

function enableStage1Scraping() {
    mainTag.setAttribute('class', 'stage1Scraping');
    stageTitleTag.textContent = "Scraping using default keyword list";

    let i = 0;
    const counterIncrease = setInterval(() => {
        if(i < 4380000) {
            i += 10000;
            tweetsFoundCounterTag.textContent = i;
        } else {
            tweetsFoundCounterTag.textContent = 4387498;
            stage1ScrapingButtonTag.classList.remove("loading");
            stage1ScrapingButtonTag.classList.add("continue");
            clearInterval(counterIncrease);
        }
    }, 1);
}

async function enableStage2Records() {
    mainTag.setAttribute('class', 'stage2Records');
    stageTitleTag.textContent = "Finding suspected accounts from live data";

    headerStageCounterTags[0].setAttribute('class',"inactive");
    headerStageCounterTags[1].setAttribute('class',"active");

    let i = 0;
    const data = await fetch(accountsFoundJSONpath)
        .then(res => res.json());
    const addRecordsToTable = setInterval(() => {
        if(i < data.length){

            // stage2RecordsTableTag.insertAdjacentHTML("beforeend",`
            //     <tr>
            //         <td>${data[i].id}</td>
            //         <td>${data[i].username}</td>
            //         <td>${data[i].tweet}</td>
            //     </tr>
            // `)
            stage2RecordsTableBodyTag.insertRow(i).insertAdjacentHTML("beforeend",`
                <td>${data[i].id}</td>
                <td>${data[i].username}</td>
                <td>${data[i].tweet}</td>
            `);
            i++;
        } else {
            stage2RecordsButtonTag.classList.remove("loading");
            stage2RecordsButtonTag.classList.add("continue");
            clearInterval(addRecordsToTable);
        }
    },20);
}

function enableStage3Network() {
    mainTag.setAttribute('class', 'stage3Network');
    stageTitleTag.textContent = "Networking based analysis on the suspected accounts";

    headerStageCounterTags[1].setAttribute('class',"inactive");
    headerStageCounterTags[2].setAttribute('class',"active");

    drawNetworkChart()

    stage3NetworkButtonTag.classList.remove("loading");
    stage3NetworkButtonTag.classList.add("continue");
}

function drawNetworkChart() {
    fetch(networkChartJSONpath).then(res => res.json()).then(data => {
        const chart = anychart.graph(data);
        chart.container("container").draw();
        chart.nodes().labels().enabled(true);
        chart.nodes().labels().format("{%id}");
        chart.nodes().labels().fontSize(14);
        chart.nodes().labels().fontFamily("Arial");
    })
    // anychart.data.loadJsonFile('./network.json', function (data) {
    // })
}

async function enableStage4Sus() {
    mainTag.setAttribute('class', 'stage4Sus');
    stageTitleTag.textContent = "Highly suspected accounts found";

    headerStageCounterTags[2].setAttribute('class',"inactive");
    headerStageCounterTags[3].setAttribute('class',"active");

    let i = 0;
    const data = await fetch(susAccountsFoundJSONpath)
        .then(res => res.json());
    const addRecordsToTable = setInterval(() => {
        if(i < data.length){

            // stage2RecordsTableTag.insertAdjacentHTML("beforeend",`
            //     <tr>
            //         <td>${data[i].id}</td>
            //         <td>${data[i].username}</td>
            //         <td>${data[i].tweet}</td>
            //     </tr>
            // `)
            stage4SusTableBodyTag.insertRow(i).insertAdjacentHTML("beforeend",`
                <td>${data[i].id}</td>
                <td>${data[i].username}</td>
            `);
            i++;
        } else {
            clearInterval(addRecordsToTable);
        }
    },20);
}