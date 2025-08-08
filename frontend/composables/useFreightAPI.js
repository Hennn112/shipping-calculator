// composables/useFreightAPI.js
export const useFreightAPI = () => {
  const config = useRuntimeConfig();

  // Base URL dari environment atau default
  const BASE_URL = config.public.apiBase || "http://localhost:8000/api";

  // Get all countries
  const getCountries = async (searchQuery = "") => {
    try {
      const params = searchQuery
        ? `?search=${encodeURIComponent(searchQuery)}`
        : "";
      const response = await $fetch(`${BASE_URL}/countries/${params}`);
      return {
        success: true,
        data: response.results || response,
        error: null,
      };
    } catch (error) {
      console.error("Failed to fetch countries:", error);
      return {
        success: false,
        data: [],
        error: error.data?.detail || "Failed to load countries",
      };
    }
  };

  // Get categories by country
  const getCategories = async (countryId, searchQuery = "") => {
    try {
      if (!countryId) {
        return { success: true, data: [], error: null };
      }

      const params = new URLSearchParams();
      params.append("country_id", countryId);
      if (searchQuery) {
        params.append("search", searchQuery);
      }

      const response = await $fetch(`${BASE_URL}/categories/?${params}`);
      return {
        success: true,
        data: response.results || response,
        error: null,
      };
    } catch (error) {
      console.error("Failed to fetch categories:", error);
      return {
        success: false,
        data: [],
        error: error.data?.detail || "Failed to load categories",
      };
    }
  };

  // Search destinations
  const searchDestinations = async (keyword) => {
    try {
      if (!keyword || keyword.length < 3) {
        return { success: true, data: [], error: null };
      }

      const response = await $fetch(
        `${BASE_URL}/destination/search/?keyword=${encodeURIComponent(keyword)}`
      );
      return {
        success: true,
        data: response.data || [],
        error: null,
      };
    } catch (error) {
      console.error("Failed to search destinations:", error);
      return {
        success: false,
        data: [],
        error: error.data?.detail || "Failed to search destinations",
      };
    }
  };

  // Calculate shipping cost
  const calculateShipping = async (params) => {
    try {
      const { countryId, categoryId, weight, destinationId } = params;

      // Validate required parameters
      if (!countryId || !categoryId || !weight || !destinationId) {
        throw new Error("All parameters are required");
      }

      const queryParams = new URLSearchParams({
        country_id: countryId,
        category_id: categoryId,
        weight: weight,
        destination_subdistrict_id: destinationId,
      });

      const response = await $fetch(`${BASE_URL}/calculate/?${queryParams}`);

      return {
        success: true,
        data: response,
        error: null,
      };
    } catch (error) {
      console.error("Failed to calculate shipping:", error);
      return {
        success: false,
        data: null,
        error:
          error.data?.error ||
          error.message ||
          "Failed to calculate shipping cost",
      };
    }
  };

  return {
    getCountries,
    getCategories,
    searchDestinations,
    calculateShipping,
  };
};
