import { useEffect } from "react"
import useApi from "./useApi";

const encodeGetParams = p => Object.entries(p).map(kv => kv.map(encodeURIComponent).join("=")).join("&");

const useSearch = params => {
    const [results, call] = useApi("/api/lookup?" + encodeGetParams(params));

    useEffect(call, [call]);

    /*
    const results = [
        {
            "score": 10.08,
            "description": "Average length of a car",
            "value": 4.6,
            "unit": "m",
            "why": "Approximate match",
            "absolute_error": 0.4,
            "relative_error": 0.08
        },
        {
            "score": 13.2,
            "description": "Number of players in a football team",
            "value": 11,
            "unit": "none",
            "why": "Half of",
            "absolute_error": 6,
            "relative_error": 1.2
        },
        {
            "score": 20.4,
            "description": "Time of a Eurovision contest song",
            "value": 3,
            "unit": "min",
            "why": "Same order of magnitude",
            "absolute_error": 2,
            "relative_error": 0.4
        },
        {
            "score": 20.65,
            "description": "Average length of a human",
            "value": 1.77,
            "unit": "m",
            "why": "Same order of magnitude",
            "absolute_error": 3.23,
            "relative_error": 0.65
        }
    ]
    */

    return results;
}

export default useSearch;