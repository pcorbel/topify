<template>
  <v-card>
    <v-card-title>
      <v-checkbox
        v-model="show_idle"
        label="Show idle processes"
        color="primary"
      />
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="processes"
      :search="search"
      :pagination.sync="pagination"
      class="elevation-1"
    >
      <template slot="headerCell" slot-scope="props">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <span v-on="on">
              {{ props.header.text }}
            </span>
          </template>
          <span>
            {{ props.header.tooltip }}
          </span>
        </v-tooltip>
      </template>
      <template v-slot:items="props">
        <td class="text-xs">{{ props.item.pid }}</td>
        <td class="text-xs">{{ props.item.username }}</td>
        <td class="text-xs">{{ props.item.nice }}</td>
        <td class="text-xs">
          <v-chip
            :color="statusToColor(props.item.status)"
            label
            small
            text-color="white"
          >
            {{ props.item.status }}
          </v-chip>
        </td>
        <td class="text-xs">{{ props.item.cpu_percent.toFixed(2) }}</td>
        <td class="text-xs">
          {{ props.item.memory_percent.toFixed(2) }}
        </td>
        <td class="text-xs">
          {{ cpuTimesToTimePlus(props.item.cpu_times) }}
        </td>
        <td class="text-xs">{{ byteFormat(props.item.memory_vms) }}</td>
        <td class="text-xs">{{ byteFormat(props.item.memory_rss) }}</td>
        <td class="text-xs">{{ props.item.name }}</td>
        <td class="text-xs">{{ props.item.cmdline.join(" ") }}</td>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import moment from "moment";
export default {
  data() {
    return {
      search: "",
      show_idle: false,
      headers: [
        {
          text: "Process ID",
          sortable: true,
          value: "pid",
          tooltip: this.$t("process_table.pid")
        },
        {
          text: "User",
          sortable: true,
          value: "username",
          tooltip: this.$t("process_table.username")
        },
        {
          text: "Nice",
          sortable: true,
          value: "nice",
          tooltip: this.$t("process_table.nice")
        },
        {
          text: "Status",
          sortable: true,
          value: "status",
          tooltip: this.$t("process_table.status")
        },
        {
          text: "CPU%",
          sortable: true,
          value: "cpu_percent",
          tooltip: this.$t("process_table.cpu_percent")
        },
        {
          text: "MEM%",
          sortable: true,
          value: "memory_percent",
          tooltip: this.$t("process_table.memory_percent")
        },
        {
          text: "CPU Times",
          sortable: false,
          value: "cpu_times",
          tooltip: this.$t("process_table.cpu_times")
        },
        {
          text: "Virtual Memory (VMS)",
          sortable: true,
          value: "memory_vms",
          tooltip: this.$t("process_table.memory_vms")
        },
        {
          text: "Physical Memory (RSS)",
          sortable: true,
          value: "memory_rss",
          tooltip: this.$t("process_table.memory_rss")
        },
        {
          text: "Name",
          sortable: true,
          value: "name",
          tooltip: this.$t("process_table.name")
        },
        {
          text: "Command",
          sortable: true,
          value: "cmdline",
          tooltip: this.$t("process_table.cmdline")
        }
      ],
      pagination: {
        sortBy: "cpu_percent",
        descending: true,
        rowsPerPage: 10
      }
    };
  },
  computed: {
    processes() {
      return this.show_idle
        ? this.$store.state.process.processes
        : this.$store.getters.processesIdleFiltered;
    }
  },
  methods: {
    cpuTimesToTimePlus(times) {
      let cpuTimesSum = times.reduce((acc, val) => acc + val, 0);
      return (
        moment
          .duration(cpuTimesSum, "seconds")
          .asHours()
          .toFixed(0) +
        "h" +
        moment.duration(cpuTimesSum, "seconds").minutes() +
        "." +
        moment.duration(cpuTimesSum, "seconds").seconds()
      );
    },
    statusToColor(state) {
      if (state === "running") {
        return "green";
      } else if (state === "sleeping") {
        return "orange";
      } else {
        return "red";
      }
    },
    byteFormat: function(input) {
      let fileSizeInBytes = input;
      let i = -1;
      let byteUnits = [" kB", " MB", " GB", " TB", "PB", "EB", "ZB", "YB"];
      do {
        fileSizeInBytes = fileSizeInBytes / 1024;
        i++;
      } while (fileSizeInBytes > 1024);
      return Math.max(fileSizeInBytes, 0.1).toFixed(1) + byteUnits[i];
    }
  }
};
</script>
