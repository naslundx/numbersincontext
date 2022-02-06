import { useEffect } from "react"
import useApi from "./useApi";

const encodeGetParams = p => Object.entries(p).map(kv => kv.map(encodeURIComponent).join("=")).join("&");

const useSearch = params => {
    const [results, call] = useApi("/api/lookup?" + encodeGetParams(params));

    useEffect(call, [call]);

    return results;
}

export default useSearch;