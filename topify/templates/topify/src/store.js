import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    cpu: {},
    disk: {},
    docker: {},
    host: {},
    memory: {},
    network: {},
    process: {},
    env: {}
  },
  mutations: {
    updateCPU(state, cpu) {
      state.cpu = cpu;
    },
    updateDisk(state, disk) {
      state.disk = disk;
    },
    updateDocker(state, docker) {
      state.docker = docker;
    },
    updateHost(state, host) {
      state.host = host;
    },
    updateMemory(state, memory) {
      state.memory = memory;
    },
    updateNetwork(state, network) {
      state.network = network;
    },
    updateProcess(state, process) {
      state.process = process;
    },
    updateEnv(state, env) {
      state.env = env;
    }
  },
  methods: {
    byteFormat(input) {
      let fileSizeInBytes = input;
      let i = -1;
      let byteUnits = [" kB", " MB", " GB", " TB", "PB", "EB", "ZB", "YB"];
      do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
      } while (fileSizeInBytes > 1024);
      return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
    }
  },
  actions: {
    // Get Data from the API
    async fetchData() {
      axios
        .get(process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_DOCKER)
        .then(docker => {
          this.commit("updateDocker", docker.data ? docker.data : {});
        });

      axios
        .get(
          process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_PROCESS
        )
        .then(process => {
          this.commit("updateProcess", process.data ? process.data : {});
        });

      axios
        .get(process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_CPU)
        .then(cpu => {
          this.commit("updateCPU", cpu.data ? cpu.data : {});
        });

      axios
        .get(process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_MEMORY)
        .then(memory => {
          this.commit("updateMemory", memory.data ? memory.data : {});
        });

      axios
        .get(process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_HOST)
        .then(host => {
          this.commit("updateHost", host.data ? host.data : {});
        });

      axios
        .get(
          process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_NETWORK
        )
        .then(network => {
          this.commit("updateNetwork", network.data ? network.data : {});
        });

      axios
        .get(process.env.VUE_APP_ROOT_API + process.env.VUE_APP_ENDPOINT_ENV)
        .then(env => {
          this.commit("updateEnv", env.data ? env.data : {});
        });
    }
  },
  getters: {
    processesIdleFiltered: state => {
      if (state.process.hasOwnProperty("processes")) {
        return state.process.processes.filter(
          process => process.status != "idle"
        );
      }
    }
  }
});
