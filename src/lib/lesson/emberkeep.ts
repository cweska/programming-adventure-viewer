import raw from "../../../content/emberkeep/first-words.json";
import { moduleSchema, type Module } from "./schema";

export const emberkeepModule: Module = moduleSchema.parse(raw);
