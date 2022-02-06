import useSearch from "../hooks/useSearch"

const ResultItem = ({ data }) => {
    return (
        <p><b>{data.why}</b>: {data.description}</p>
    )
}

const Results = ({ searchTerms }) => {
    const searchResults = useSearch(searchTerms);

    return (
        <div className="result">
            {searchResults.map(e => <ResultItem data={e} />)}
        </div>
    )
}

export default Results;