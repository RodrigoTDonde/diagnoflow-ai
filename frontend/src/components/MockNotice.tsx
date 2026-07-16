type MockNoticeProps = {
  title: string;
  description: string;
  badgeLabel?: string;
};

export function MockNotice({ title, description, badgeLabel = "Fluxo da aplicação" }: MockNoticeProps) {
  return (
    <section className="mock-notice" aria-label="Aviso contextual da aplicação">
      <span className="badge badge-warning">{badgeLabel}</span>
      <div>
        <strong>{title}</strong>
        <p>{description}</p>
      </div>
    </section>
  );
}
