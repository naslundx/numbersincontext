import { useCallback, useEffect, useState } from "react"

const useApi = (url) => {
    const [data, setData] = useState([]);

    const call = useCallback(async () => {
        console.log(url);
        const response = await fetch(url);
        if (response.status != 200) {
            setData([]);
        } else {
            const json = await response.json();
            setData(json);
        }
    }, [setData, url])

    return [data, call];
}

export default useApi;