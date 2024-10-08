package com.comet.opik.infrastructure.db;

import com.comet.opik.infrastructure.DatabaseAnalyticsFactory;
import com.comet.opik.infrastructure.OpikConfiguration;
import com.google.inject.Provides;
import io.r2dbc.spi.ConnectionFactory;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import ru.vyarus.dropwizard.guice.module.support.DropwizardAwareModule;

public class DatabaseAnalyticsModule extends DropwizardAwareModule<OpikConfiguration> {

    private transient DatabaseAnalyticsFactory databaseAnalyticsFactory;
    private transient ConnectionFactory connectionFactory;

    @Override
    protected void configure() {
        databaseAnalyticsFactory = configuration(DatabaseAnalyticsFactory.class);
        connectionFactory = databaseAnalyticsFactory.build();
    }

    @Provides
    @Singleton
    public ConnectionFactory getConnectionFactory() {
        return connectionFactory;
    }

    @Provides
    @Singleton
    @Named("Database Analytics Database Name")
    public String getDatabaseName() {
        return databaseAnalyticsFactory.getDatabaseName();
    }

    @Provides
    @Singleton
    public TransactionTemplateAsync getTransactionTemplate(ConnectionFactory connectionFactory) {
        return new TransactionTemplateAsyncImpl(connectionFactory);
    }

}
