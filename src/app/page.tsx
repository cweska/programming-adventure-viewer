import { ModulePicker } from "../components/ModulePicker";
import { studentModules } from "../lib/lesson/modules";

export default function Page() {
  return <ModulePicker modules={studentModules()} />;
}
