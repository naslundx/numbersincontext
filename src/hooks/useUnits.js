import { useEffect } from "react"
import useApi from "./useApi";

const useUnits = () => {
    const [units, call] = useApi('/api/units');

    useEffect(call, [call]);    

    return units;
}

export default useUnits;