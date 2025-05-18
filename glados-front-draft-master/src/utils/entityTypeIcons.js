import AirConditionerIcon from "vue-material-design-icons/AirConditioner.vue"
import HelpIcon from "vue-material-design-icons/HelpCircle.vue"
import LightbulbIcon from "vue-material-design-icons/Lightbulb.vue"
import MonitorIcon from "vue-material-design-icons/Monitor.vue"
import ThermometerIcon from "vue-material-design-icons/Thermometer.vue"
import ToggleSwitchIcon from "vue-material-design-icons/ToggleSwitch.vue"


const typeIcons = {
  "light": LightbulbIcon,
  "sensor": ThermometerIcon,
  "switch": ToggleSwitchIcon,
  "multimedia": MonitorIcon,
  "air_conditioner": AirConditionerIcon
}

export default function getTypeIcon(typeName) {
  return typeIcons[typeName] || HelpIcon
}