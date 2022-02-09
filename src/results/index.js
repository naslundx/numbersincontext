import useSearch from "../hooks/useSearch"
import ResultItem from "./ResultItem";
import "./results.css"

const Results = ({ searchTerms }) => {
    const searchResults = useSearch(searchTerms);
    const className = "result transparentbox" + (searchResults.length === 0 ? "" : " withcontent");

    return (
        <div className={className}>
            {searchResults.map(e => <ResultItem key={e.id} data={e} />)}
            {searchResults.length === 0 && <p>Enter a number...</p>}
        </div>
    )
}

export default Results;