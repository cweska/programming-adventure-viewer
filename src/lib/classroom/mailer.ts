import nodemailer from "nodemailer";

export type EmailMessage = {
  to: string;
  subject: string;
  text: string;
};

export interface Mailer {
  send(message: EmailMessage): void | Promise<unknown>;
}

export type AppEnv = Record<string, string | undefined>;

export function isSmtpConfigured(env: AppEnv): boolean {
  return Boolean(env.SMTP_HOST && env.SMTP_PORT && env.SMTP_FROM);
}

export function createSmtpMailer(env: AppEnv): Mailer | null {
  if (!isSmtpConfigured(env)) return null;
  const port = Number(env.SMTP_PORT);
  const transport = nodemailer.createTransport({
    host: env.SMTP_HOST,
    port,
    secure: env.SMTP_SECURE === "true" || port === 465,
    auth: env.SMTP_USER
      ? {
          user: env.SMTP_USER,
          pass: env.SMTP_PASS,
        }
      : undefined,
  });
  return {
    send(message) {
      return transport.sendMail({
        from: env.SMTP_FROM,
        to: message.to,
        subject: message.subject,
        text: message.text,
      });
    },
  };
}
