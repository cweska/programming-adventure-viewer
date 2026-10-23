import raw from "../../../content/modules/emberkeep/first-words.json";
import { moduleSchema, type Module } from "./schema";

export const emberkeepModule: Module = moduleSchema.parse(raw);
