<template>
  <v-app id="project">
    <v-container grid-list-xl fill-height>
      <v-layout row wrap>
        <v-flex xs12>
          <mini-statistic
            icon="mdi-file-tree"
            :title="mini_statistic_title"
            :sub-title="mini_statistic_subtitle"
            color="green"
          />
        </v-flex>
        <v-flex xs12>
          <the-hardware-table />
        </v-flex>
        <v-flex xs12>
          <the-process-table />
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import MiniStatistic from "@/components/MiniStatistic";
import TheHardwareTable from "@/components/TheHardwareTable";
import TheProcessTable from "@/components/TheProcessTable";
export default {
  components: {
    MiniStatistic,
    TheHardwareTable,
    TheProcessTable
  },
  computed: {
    mini_statistic_title() {
      let title = "Processes: ";
      if (this.$store.state.process.hasOwnProperty("processes")) {
        title += this.$store.state.process.processes.length;
      }
      return title;
    },
    mini_statistic_subtitle() {
      var _ = require("lodash");
      return (
        "Load Average: " +
        _.get(this.$store.state.host, "load_avg_1", 0).toFixed(2) +
        " " +
        _.get(this.$store.state.host, "load_avg_5", 0).toFixed(2) +
        " " +
        _.get(this.$store.state.host, "load_avg_15", 0).toFixed(2)
      );
    }
  }
};
</script>
