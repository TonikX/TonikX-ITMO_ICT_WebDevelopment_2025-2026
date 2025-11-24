package io.github.artsobol.kurkod.web.domain.report.farm.projection;

public interface BreedWorkshopMonthlyProjection {

    Long getWorkshopId();

    Integer getWorkshopNumber();

    Long getBreedId();

    String getBreedName();

    Long getChickensCount();

    Long getEggsTotal();

    java.math.BigDecimal getAvgEggsPerChicken();
}