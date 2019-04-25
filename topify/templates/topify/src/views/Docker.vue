<template>
  <v-app id="project">
    <v-container grid-list-xl>
      <v-layout row wrap>
        <v-flex xs12>
          <mini-statistic
            icon="mdi-docker"
            :title="mini_statistic_title"
            :sub-title="mini_statistic_subtitle"
            color="green"
          />
        </v-flex>
        <v-flex xs12>
          <the-docker-containers-table />
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import MiniStatistic from "@/components/MiniStatistic";
import TheDockerContainersTable from "@/components/TheDockerContainersTable";
export default {
  components: {
    MiniStatistic,
    TheDockerContainersTable
  },
  computed: {
    mini_statistic_title() {
      var _ = require("lodash");
      return (
        "Docker " +
        _.get(this.$store.state.docker, "server.license") +
        " (" +
        _.get(this.$store.state.docker, "server.version") +
        ")"
      );
    },
    mini_statistic_subtitle() {
      var _ = require("lodash");
      return _.get(this.$store.state.docker, "server.os");
    }
  }
};
</script>
