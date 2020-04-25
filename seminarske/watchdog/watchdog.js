const delay  = require('delay');

const work = async(endless) => {

    var i = 0;

    console.log("Starting endless loop: " + endless);
    while (endless) {
        i++;
        await delay();
    }
};

const main = async (endless) => {
    console.error("============================ MAIN");

    console.log("Watchdog started...");
    timeout = setTimeout(() => {
        console.error("============================ WATCHDOG");
        console.error("Endless loop detected...");
        console.error("Exiting main loop...");
        console.error("============================ END WATCHDOG");
        process.exit(3);
    }, 4 * 1000);

    await work(endless);

    clearTimeout(timeout);
    console.log("Exit loop!");
    console.error("============================ END MAIN");
};

module.exports = main;

