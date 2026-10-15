import raw from "../../../content/emberkeep/gate.json";
import { moduleSchema, type Module } from "./schema";

export const emberkeepModule: Module = moduleSchema.parse(raw);
