<template>
  <v-toolbar color="primary" fixed dark app>
    <v-toolbar-title>
      <span>{{ host.node }} ({{ network.public_ip }})</span>
    </v-toolbar-title>
    <v-spacer />
    <span>Uptime: {{ uptime }}</span>
  </v-toolbar>
</template>

<script>
import moment from "moment";
export default {
  computed: {
    host() {
      return this.$store.state.host;
    },
    network() {
      return this.$store.state.network;
    },
    uptime() {
      let uptime = moment.duration(this.$store.state.host.up_time, "seconds");
      return (
        Math.floor(uptime.asDays()) +
        " days " +
        uptime
          .hours()
          .toString()
          .padStart(2, "0") +
        ":" +
        uptime
          .minutes()
          .toString()
          .padStart(2, "0") +
        ":" +
        uptime
          .seconds()
          .toString()
          .padStart(2, "0")
      );
    }
  }
};
</script>
