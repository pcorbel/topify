<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
      />
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="items"
      :search="search"
      :rows-per-page-items="[
        { text: '$vuetify.dataIterator.rowsPerPageAll', value: 10 },
        10,
        25,
        100
      ]"
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
        <td class="text-xs">{{ props.item.name }}</td>
        <td class="text-xs">
          <v-chip label small color="blue" text-color="white">
            {{ props.item.short_id }}
          </v-chip>
        </td>
        <td class="text-xs">
          <v-chip
            :color="stateToColor(props.item.state)"
            small
            text-color="white"
          >
            {{ props.item.state }}
          </v-chip>
        </td>
        <td class="text-xs">{{ props.item.status }}</td>
        <td class="text-xs">
          <kbd>{{ props.item.image }}</kbd>
        </td>
        <td class="text-xs">
          <code>{{ props.item.cmd }}</code>
        </td>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      headers: [
        {
          text: "Name",
          sortable: true,
          value: "name",
          tooltip: this.$t("container_table.name")
        },
        {
          text: "Short ID",
          sortable: true,
          value: "short_id",
          tooltip: this.$t("container_table.short_id")
        },
        {
          text: "State",
          sortable: true,
          value: "state",
          tooltip: this.$t("container_table.state")
        },
        {
          text: "Status",
          sortable: true,
          value: "status",
          tooltip: this.$t("container_table.status")
        },
        {
          text: "Image",
          sortable: true,
          value: "image",
          tooltip: this.$t("container_table.image")
        },
        {
          text: "Command",
          sortable: true,
          value: "cmd",
          tooltip: this.$t("container_table.cmd")
        }
      ]
    };
  },
  computed: {
    items() {
      return this.$store.state.docker.containers;
    }
  },
  methods: {
    stateToColor(state) {
      if (state === "running") {
        return "green";
      } else if (state === "exited" || state === "dead") {
        return "red";
      } else {
        return "orange";
      }
    }
  }
};
</script>
