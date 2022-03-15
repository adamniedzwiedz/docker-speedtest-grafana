const execa = require("execa");
const Influx = require("influx");
const delay = require("delay");
const util = require('util');

const SPEEDTEST_SERVER = process.env.SPEEDTEST_SERVER;
const SPEEDTEST_HOST = process.env.SPEEDTEST_HOST ?? 'local';
const SPEEDTEST_INTERVAL = process.env.SPEEDTEST_INTERVAL ?? 3600;
const MTR_HOST = process.env.MTR_HOST ?? '8.8.8.8'
const MTR_INTERVAL = process.env.MTR_INTERVAL ?? 120;

const influx = new Influx.InfluxDB({
  host: process.env.INFLUXDB_HOST ?? 'influxdb',
  database: process.env.INFLUXDB_DB ?? 'speedtest',
  username: process.env.INFLUXDB_USERNAME ?? 'root',
  password: process.env.INFLUXDB_PASSWORD ?? 'root',
});

const bitToMbps = bit => (bit / 1000 / 1000) * 8;

const log = (message, severity = "Info") =>
    console.log(`[${severity.toUpperCase()}][${new Date()}] ${message}`);

const getSpeedMetrics = async () => {
  const args = (SPEEDTEST_SERVER) ?
      [ "--accept-license", "--accept-gdpr", "-f", "json", "--server-id=" + SPEEDTEST_SERVER] :
      [ "--accept-license", "--accept-gdpr", "-f", "json" ];

  const { stdout } = await execa("speedtest", args);
  const result = JSON.parse(stdout);
  return {
    upload: bitToMbps(result.upload.bandwidth),
    download: bitToMbps(result.download.bandwidth),
    ping: result.ping.latency
  };
};

const getMtrResult = async () => {
  const args = [ "-r", MTR_HOST ];

  const { stdout } = await execa("mtr", args);
  const mtrData = new RegExp(".*--\\s*([\\w|\\.]+)\\s*([\\d|\\.]+)%\\s*([\\d|\\.]+)\\s*([\\d|\\.]+)\\s*([\\d|\\.]+)\\s*([\\d|\\.]+)\\s*([\\d|\\.]+)\\s*([\\d|\\.]+)");
  const lastHop = stdout.split("\n").slice(-1).toString();
  const match = lastHop.match(mtrData);

  let result = {};
  const fields = ['loss', 'snt', 'last', 'avg', 'best', 'worst', 'stdev'];

  match.slice(2).forEach((value, i) => result[fields[i]] = Number(value));
  return result;
};

const pushToInflux = async (metrics) => {
  const points = Object.entries(metrics).map(([measurement, value]) => ({
    measurement,
    tags: { host: SPEEDTEST_HOST },
    fields: { value }
  }));
  await influx.writePoints(points);
};

const run = async (name, method, wait_sec) => {
  try {
    while (true) {
      log(`Starting ${name}...`);
      const result = await method();
      log(util.inspect(result, {showHidden: false, depth: null, colors: true}));
      await pushToInflux(result);

      log(`${name} sleeping for ${wait_sec} seconds...`);
      await delay(wait_sec * 1000);
    }
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
};

(async () => {
  await run("speedtest", getSpeedMetrics, SPEEDTEST_INTERVAL);
})();

(async () => {
  await run("mtr", getMtrResult, MTR_INTERVAL);
})();
